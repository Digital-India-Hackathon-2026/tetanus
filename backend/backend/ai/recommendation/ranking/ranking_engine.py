import json
import os
import time
from typing import List, Tuple, Dict, Any, Optional

from backend.ai.recommendation.models import CandidateProduct, RecommendationContext
from backend.ai.mission.mission_models import MissionContext
from backend.ai.recommendation.ranking.ranking_models import (
    ScoredProduct, ScoreBreakdown, ScoreComponent,
    RankingReport, PerScorerTelemetry
)
from backend.ai.recommendation.ranking.scoring_rules import (
    ScorerRegistry, BoostEngine, PenaltyEngine, RankingReasonBuilder
)

# Ensure all scorers are registered by importing scoring_rules
import backend.ai.recommendation.ranking.scoring_rules  # noqa: F401


class RankingEngine:
    SCORER_KEY_MAP = {
        "mission_match": "mission_match",
        "budget_match": "budget_match",
        "quality_score": "quality_score",
        "rating": "rating",
        "review_count": "review_count",
        "brand_preference": "brand_preference",
        "category_priority": "category_priority",
    }

    def __init__(self, config_path: Optional[str] = None, profile: Optional[str] = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "ranking_config.json")
        with open(config_path, "r") as f:
            full_config = json.load(f)

        self.profile = profile or full_config.get("default_profile", "balanced")
        self.config = full_config["profiles"][self.profile]
        self.config["thresholds"] = full_config.get("thresholds", {})
        self.config["intent_bonus_map"] = full_config.get("intent_bonus_map", {})
        self.boost_engine = BoostEngine()
        self.penalty_engine = PenaltyEngine()
        self.reason_builder = RankingReasonBuilder()

    def rank(
        self,
        products: List[CandidateProduct],
        mission_context: MissionContext,
        recommendation_context: RecommendationContext
    ) -> Tuple[List[ScoredProduct], RankingReport]:
        pipeline_start = time.time()
        report = RankingReport(profile_used=self.profile)

        if not products:
            return [], report

        scorer_timings: Dict[str, List[float]] = {k: [] for k in self.config["weights"].keys()}
        scorer_contributions: Dict[str, List[float]] = {k: [] for k in self.config["weights"].keys()}

        scored: List[ScoredProduct] = []

        for product in products:
            breakdown = self._score_product(
                product, mission_context, recommendation_context, scorer_timings, scorer_contributions
            )
            sp = ScoredProduct(
                product_id=product.product_id,
                name=product.name,
                brand=product.brand,
                category=product.category,
                price=product.price,
                rating=product.rating,
                review_count=product.review_count,
                quality_score=product.quality_score,
                description=product.description,
                image_url=product.image_url,
                product_url=product.product_url,
                inventory=product.inventory,
                score_breakdown=breakdown,
                final_score=breakdown.final_score,
                metadata=product.metadata,
            )
            scored.append(sp)

        scored.sort(key=lambda s: s.final_score, reverse=True)

        # Build report
        scores = [s.final_score for s in scored]
        report.products_ranked = len(scored)
        report.execution_time_ms = (time.time() - pipeline_start) * 1000
        report.top_score = max(scores) if scores else 0.0
        report.lowest_score = min(scores) if scores else 0.0
        report.average_score = sum(scores) / len(scores) if scores else 0.0
        report.score_distribution = self._compute_distribution(scores)

        for scorer_key, timings in scorer_timings.items():
            contributions = scorer_contributions.get(scorer_key, [])
            report.per_scorer_telemetry.append(PerScorerTelemetry(
                scorer_name=scorer_key,
                execution_time_ms=sum(timings) * 1000,
                average_contribution=sum(contributions) / len(contributions) if contributions else 0.0
            ))

        return scored, report

    def _score_product(
        self,
        product: CandidateProduct,
        mission_context: MissionContext,
        recommendation_context: RecommendationContext,
        scorer_timings: Dict,
        scorer_contributions: Dict
    ) -> ScoreBreakdown:
        components: List[ScoreComponent] = []

        for scorer_key in self.config["weights"].keys():
            try:
                scorer = ScorerRegistry.get_scorer(scorer_key)
            except ValueError:
                continue

            t0 = time.time()
            result = scorer.score(product, mission_context, recommendation_context, self.config)
            elapsed = time.time() - t0
            scorer_timings[scorer_key].append(elapsed)
            scorer_contributions[scorer_key].append(result.weighted_score)

            components.append(ScoreComponent(
                scorer_name=result.scorer_name,
                raw_score=result.raw_score,
                weighted_score=result.weighted_score,
                weight=self.config["weights"][scorer_key],
                explanation=result.explanation
            ))

        base_score = min(1.0, sum(c.weighted_score for c in components))

        # Apply boosts (additive, clamped)
        after_boost, boosts_applied = self.boost_engine.apply(
            base_score, product, mission_context, recommendation_context, self.config
        )
        after_boost = min(1.0, after_boost)

        # Apply penalties (additive deductions, clamped)
        final, penalties_applied = self.penalty_engine.apply(after_boost, product, self.config)
        final = max(0.0, min(1.0, final))

        breakdown = ScoreBreakdown(
            base_score=base_score,
            components=components,
            boosts_applied=boosts_applied,
            penalties_applied=penalties_applied,
            after_boost_score=after_boost,
            final_score=final
        )
        breakdown.top_reasons = self.reason_builder.build(breakdown)

        return breakdown

    def _compute_distribution(self, scores: List[float]) -> Dict[str, int]:
        dist = {"0.0-0.2": 0, "0.2-0.4": 0, "0.4-0.6": 0, "0.6-0.8": 0, "0.8-1.0": 0}
        for s in scores:
            if s < 0.2:
                dist["0.0-0.2"] += 1
            elif s < 0.4:
                dist["0.2-0.4"] += 1
            elif s < 0.6:
                dist["0.4-0.6"] += 1
            elif s < 0.8:
                dist["0.6-0.8"] += 1
            else:
                dist["0.8-1.0"] += 1
        return dist
