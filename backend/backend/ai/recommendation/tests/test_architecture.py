import pytest
from backend.ai.recommendation.recommendation_service import RecommendationService
from backend.ai.recommendation.models import CandidateProduct, RecommendedProduct, RecommendedBundle, RecommendationResponse, RecommendationContext
from backend.ai.recommendation.exceptions import RecommendationError
from backend.ai.recommendation.retrieval.graph_repository import Neo4jGraphRepository
from backend.ai.recommendation.filtering.filters import BaseFilter
from backend.ai.recommendation.ranking.scorer import RankingInterface
from backend.ai.recommendation.diversity.diversity import DiversityInterface
from backend.ai.recommendation.bundling.bundle_builder import BundleBuilderInterface
from backend.ai.mission.mission_models import MissionContext, MissionMetadata

class DummyFilter(BaseFilter):
    def apply(self, products, mission_context, recommendation_context, config):
        return products, []

class DummyRanking(RankingInterface):
    def score_products(self, products, context):
        return products

class DummyDiversity(DiversityInterface):
    def enforce_diversity(self, products, context):
        return products

class DummyBundleBuilder(BundleBuilderInterface):
    def build_bundles(self, products, context):
        return []

def test_architecture_interfaces():
    assert issubclass(Neo4jGraphRepository, object)

def test_recommendation_service_initialization():
    service = RecommendationService(
        graph_repo=Neo4jGraphRepository(),
        filter_layer=DummyFilter(),
        ranking_engine=DummyRanking(),
        diversity_engine=DummyDiversity(),
        bundle_builder=DummyBundleBuilder()
    )
    assert service is not None

def test_recommendation_service_pipeline():
    service = RecommendationService(
        graph_repo=Neo4jGraphRepository(),
        filter_layer=DummyFilter(),
        ranking_engine=DummyRanking(),
        diversity_engine=DummyDiversity(),
        bundle_builder=DummyBundleBuilder()
    )

    ctx = MissionContext(
        mission="Test Mission",
        supported=True,
        definition={},
        primary_categories=["C1"],
        secondary_categories=[],
        required_categories=[],
        optional_categories=[],
        category_weights={},
        bundle_ids=[],
        priority="NORMAL",
        mission_type="TEST",
        metadata=MissionMetadata(
            aikb_version="1",
            schema_version="1",
            generated_at="now",
            mission_hash="abc",
            source="test",
            loaded_from="test",
            load_time_ms=1.0
        )
    )

    rec_ctx = RecommendationContext()
    response = service.generate_recommendations("test query", ctx, rec_ctx)
    assert isinstance(response, RecommendationResponse)
    assert response.mission == "Test Mission"
    assert response.statistics is not None
    assert response.metadata is not None
