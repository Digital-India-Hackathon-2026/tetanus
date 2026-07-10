import pytest
from backend.ai.mission.mission_models import MissionMetadata

def get_mission_ctx(bundle_ids=None):
    meta = MissionMetadata(aikb_version="1.0", schema_version="1.0", generated_at="2026", mission_hash="abc", source="test", loaded_from="test", load_time_ms=1.0)
    return MissionContext(mission="test", intent_type="test", supported=True, definition={}, primary_categories=[], secondary_categories=[], required_categories=[], optional_categories=[], category_weights={}, bundle_ids=bundle_ids or [], priority="P1", mission_type="test", metadata=meta)
from unittest.mock import patch, MagicMock
from backend.ai.recommendation.bundling.bundle_builder_impl import BundleBuilder
from backend.ai.recommendation.ranking.ranking_models import ScoredProduct, ScoreBreakdown
from backend.ai.mission.mission_models import MissionContext
from backend.ai.recommendation.models import RecommendationContext
import json
import os
import tempfile

@pytest.fixture
def temp_config():
    config = {
        "max_bundles": 2,
        "min_bundle_size": 2,
        "max_bundle_size": 4
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".json") as f:
        json.dump(config, f)
        temp_path = f.name
    yield temp_path
    os.remove(temp_path)

@pytest.fixture
def bundle_builder(temp_config):
    # Mock the MissionLoader so we can inject custom bundle knowledge
    with patch('backend.ai.recommendation.bundling.bundle_builder_impl.MissionLoader') as MockLoader:
        mock_instance = MockLoader.return_value
        mock_instance.load_bundles.return_value = [
            {
                "bundle_name": "Test Bundle 1",
                "categories": ["Cat1", "Cat2", "Cat3"]
            },
            {
                "bundle_name": "Test Bundle 2",
                "products": ["Prod A", "Prod B"]
            }
        ]
        builder = BundleBuilder(config_path=temp_config)
        return builder

def test_bundling_categories(bundle_builder):
    products = [
        ScoredProduct(product_id="1", name="P1", category="Cat1", price=100.0, final_score=0.9, score_breakdown=ScoreBreakdown(base_score=1.0)),
        ScoredProduct(product_id="2", name="P2", category="Cat2", price=200.0, final_score=0.8, score_breakdown=ScoreBreakdown(base_score=1.0)),
    ]
    mission_ctx = get_mission_ctx(bundle_ids=["Test Bundle 1"])
    rec_ctx = RecommendationContext(budget=500.0)

    bundles = bundle_builder.build_bundles(products, mission_ctx, rec_ctx)
    assert len(bundles) == 1
    
    bundle = bundles[0]
    assert bundle.name == "Test Bundle 1"
    assert len(bundle.products) == 2
    assert bundle.total_price == 300.0
    assert bundle.budget_utilization == 300.0 / 500.0
    assert bundle.completeness == 2 / 3  # 2 found, 3 required
    assert "Cat3" in bundle.missing_categories

def test_bundling_exact_products(bundle_builder):
    products = [
        ScoredProduct(product_id="1", name="Prod A", category="Cat1", price=100.0, final_score=0.9, score_breakdown=ScoreBreakdown(base_score=1.0)),
        ScoredProduct(product_id="2", name="Prod B", category="Cat2", price=200.0, final_score=0.8, score_breakdown=ScoreBreakdown(base_score=1.0)),
    ]
    mission_ctx = get_mission_ctx(bundle_ids=["Test Bundle 2"])
    rec_ctx = RecommendationContext(budget=200.0)

    bundles = bundle_builder.build_bundles(products, mission_ctx, rec_ctx)
    assert len(bundles) == 1
    
    bundle = bundles[0]
    assert bundle.name == "Test Bundle 2"
    assert len(bundle.products) == 2
    assert bundle.total_price == 300.0
    assert bundle.budget_utilization == 300.0 / 200.0 # Over budget
    assert bundle.completeness == 1.0
    assert not bundle.missing_products

def test_bundling_partial(bundle_builder):
    products = [
        ScoredProduct(product_id="1", name="Prod A", category="Cat1", price=100.0, final_score=0.9, score_breakdown=ScoreBreakdown(base_score=1.0)),
        # Prod B is missing
    ]
    mission_ctx = get_mission_ctx(bundle_ids=["Test Bundle 2"])
    rec_ctx = RecommendationContext(budget=200.0)

    bundles = bundle_builder.build_bundles(products, mission_ctx, rec_ctx)
    # min_bundle_size is 2, so this bundle should not be created!
    assert len(bundles) == 0
