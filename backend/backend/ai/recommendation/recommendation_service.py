import time
import logging
from typing import List, Optional

from backend.ai.mission.mission_models import MissionContext
from backend.ai.recommendation.models import (
    CandidateProduct, RecommendedProduct, RecommendedBundle,
    RecommendationResponse, RetrievalStatistics, RecommendationMetadata,
    RecommendationContext
)
from backend.ai.recommendation.telemetry import TelemetryTracker
from backend.ai.recommendation.config import RecommendationConfig
from backend.ai.recommendation.retrieval.graph_repository import Neo4jGraphRepository
from backend.ai.recommendation.filtering.filters import FilterPipeline
from backend.ai.recommendation.ranking.ranking_engine import RankingEngine
from backend.ai.recommendation.diversity.diversity_engine import DiversityEngine
from backend.ai.recommendation.bundling.bundle_builder_impl import BundleBuilder
from backend.ai.agents.explanation_agent import ExplanationAgent

logger = logging.getLogger("CIN.RecommendationService")


class RecommendationService:
    """
    Orchestrates the full recommendation pipeline:
    Retrieval → Filtering → Ranking → Diversity → Bundling → Explanation
    """

    def __init__(
        self,
        graph_repo: Optional[Neo4jGraphRepository] = None,
        filter_layer: Optional[FilterPipeline] = None,
        ranking_engine: Optional[RankingEngine] = None,
        diversity_engine: Optional[DiversityEngine] = None,
        bundle_builder: Optional[BundleBuilder] = None,
        explanation_agent: Optional[ExplanationAgent] = None,
    ):
        self.graph_repo = graph_repo or Neo4jGraphRepository()
        self.filter_layer = filter_layer or FilterPipeline()
        self.ranking_engine = ranking_engine or RankingEngine()
        self.diversity_engine = diversity_engine or DiversityEngine()
        self.bundle_builder = bundle_builder or BundleBuilder()
        self.explanation_agent = explanation_agent or ExplanationAgent()
        self.config = RecommendationConfig()

    def generate_recommendations(
        self,
        query: str,
        mission_context: MissionContext,
        recommendation_context: RecommendationContext,
    ) -> RecommendationResponse:
        telemetry = TelemetryTracker()
        telemetry.start_timer("execution")

        if not getattr(mission_context, "supported", True):
            logger.info("Unsupported mission detected. Short-circuiting recommendation pipeline.")
            telemetry.stop_timer("execution", "execution_time_ms")
            return RecommendationResponse(
                mission=mission_context.mission,
                products=[],
                bundles=[],
                explanation="I'm sorry, but I don't currently support finding products for that kind of request. I specialize in shopping missions like hostel setups, gym gear, travel essentials, and home offices.",
                statistics=RetrievalStatistics(retrieved_count=0, filtered_count=0, returned_count=0),
                metadata=RecommendationMetadata(
                    execution_time_ms=telemetry.execution_time_ms,
                    ranking_time_ms=0, filter_time_ms=0, bundle_time_ms=0, repository_time_ms=0
                ),
                filtering_summary={}, ranking_summary={}, diversity_summary={}
            )

        # ── 1. Retrieval ────────────────────────────────────────────────────
        telemetry.start_timer("repository")
        try:
            self.graph_repo.connect()
            categories = mission_context.primary_categories + mission_context.secondary_categories
            candidates: List[CandidateProduct] = self.graph_repo.get_products_by_categories(
                categories, limit=self.config.max_candidates
            )
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            candidates = []
        telemetry.record_counts(retrieved=len(candidates))
        telemetry.stop_timer("repository", "repository_time_ms")

        # ── 2. Filtering ────────────────────────────────────────────────────
        telemetry.start_timer("filter")
        try:
            filtered_products, filter_report = self.filter_layer.run(
                candidates, mission_context, recommendation_context
            )
        except Exception as e:
            logger.error(f"Filtering failed: {e}")
            filtered_products = candidates
            filter_report = None
        telemetry.record_counts(filtered=len(candidates) - len(filtered_products))
        telemetry.stop_timer("filter", "filter_time_ms")

        # ── 3. Ranking ──────────────────────────────────────────────────────
        telemetry.start_timer("ranking")
        try:
            ranked_products, ranking_report = self.ranking_engine.rank(
                filtered_products, mission_context, recommendation_context
            )
        except Exception as e:
            logger.error(f"Ranking failed: {e}")
            ranked_products = []
            ranking_report = None
        telemetry.stop_timer("ranking", "ranking_time_ms")

        # ── 4. Diversity ────────────────────────────────────────────────────
        try:
            diverse_products, diversity_summary = self.diversity_engine.enforce(
                ranked_products, mission_context, recommendation_context
            )
        except Exception as e:
            logger.error(f"Diversity failed: {e}")
            diverse_products = ranked_products[:self.config.max_returned_products]
            diversity_summary = {"error": str(e)}

        # ── 5. Bundling ─────────────────────────────────────────────────────
        telemetry.start_timer("bundle")
        try:
            bundles: List[RecommendedBundle] = self.bundle_builder.build_bundles(
                diverse_products, mission_context, recommendation_context, self.graph_repo
            )
        except Exception as e:
            logger.warning(f"Bundle building failed: {e}")
            bundles = []
        telemetry.stop_timer("bundle", "bundle_time_ms")

        # ── 6. Explanation ──────────────────────────────────────────────────
        try:
            explanation = self.explanation_agent.generate_explanation(
                query=query,
                mission_context=mission_context,
                recommendation_context=recommendation_context,
                top_products=diverse_products[:3],
                bundles=bundles[:1] if bundles else None,
            )
        except Exception as e:
            logger.warning(f"Explanation generation failed: {e}")
            explanation = ""

        # ── 7. Assemble response ────────────────────────────────────────────
        telemetry.stop_timer("execution", "execution_time_ms")
        telemetry.record_counts(returned=len(diverse_products))

        recommended_products = [
            RecommendedProduct(
                product=sp,
                justification=" | ".join(sp.score_breakdown.top_reasons[:3])
            )
            for sp in diverse_products
        ]

        return RecommendationResponse(
            mission=mission_context.mission,
            products=recommended_products,
            bundles=bundles[:self.config.max_returned_bundles],
            explanation=explanation,
            statistics=RetrievalStatistics(
                retrieved_count=telemetry.retrieved_products,
                filtered_count=telemetry.filtered_products,
                returned_count=telemetry.returned_products,
            ),
            metadata=RecommendationMetadata(
                execution_time_ms=telemetry.execution_time_ms,
                ranking_time_ms=telemetry.ranking_time_ms,
                filter_time_ms=telemetry.filter_time_ms,
                bundle_time_ms=telemetry.bundle_time_ms,
                repository_time_ms=telemetry.repository_time_ms,
            ),
            filtering_summary=filter_report.model_dump() if filter_report else {},
            ranking_summary=ranking_report.model_dump() if ranking_report else {},
            diversity_summary=diversity_summary,
        )
