import pytest
from backend.ai.recommendation.diversity.diversity_engine import DiversityEngine
from backend.ai.recommendation.ranking.ranking_models import ScoredProduct, ScoreBreakdown
from backend.ai.mission.mission_models import MissionContext, MissionMetadata
from backend.ai.recommendation.models import RecommendationContext
import json

def get_mission_ctx():
    meta = MissionMetadata(
        aikb_version="1.0", schema_version="1.0", generated_at="2026",
        mission_hash="abc", source="test", loaded_from="test", load_time_ms=1.0
    )
    return MissionContext(
        mission="test", intent_type="test", supported=True, definition={},
        primary_categories=[], secondary_categories=[], required_categories=[],
        optional_categories=[], category_weights={}, bundle_ids=[],
        priority="P1", mission_type="test", metadata=meta
    )
import os
import tempfile

@pytest.fixture
def temp_config():
    config = {
        "max_per_brand": 2,
        "max_per_category": 3,
        "max_per_subcategory": 10,
        "max_total_results": 10
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".json") as f:
        json.dump(config, f)
        temp_path = f.name
    yield temp_path
    os.remove(temp_path)

@pytest.fixture
def diversity_engine(temp_config):
    return DiversityEngine(config_path=temp_config)

def test_diversity_duplicate_names(diversity_engine):
    products = [
        ScoredProduct(product_id="1", name="Product A", brand="Brand1", category="Cat1", price=10.0, score_breakdown=ScoreBreakdown(base_score=1.0)),
        ScoredProduct(product_id="2", name="Product A", brand="Brand2", category="Cat1", price=12.0, score_breakdown=ScoreBreakdown(base_score=1.0)),
    ]
    mission_ctx = get_mission_ctx()
    rec_ctx = RecommendationContext()

    result, summary = diversity_engine.enforce(products, mission_ctx, rec_ctx)
    assert len(result) == 1
    assert summary["drop_reasons"]["duplicate"] == 1
    assert result[0].product_id == "1"

def test_diversity_brand_limit(diversity_engine):
    products = [
        ScoredProduct(product_id="1", name="Prod1", brand="B1", category="C1", price=10.0, score_breakdown=ScoreBreakdown(base_score=1.0)),
        ScoredProduct(product_id="2", name="Prod2", brand="B1", category="C2", price=10.0, score_breakdown=ScoreBreakdown(base_score=1.0)),
        ScoredProduct(product_id="3", name="Prod3", brand="B1", category="C3", price=10.0, score_breakdown=ScoreBreakdown(base_score=1.0)),
    ]
    mission_ctx = get_mission_ctx()
    rec_ctx = RecommendationContext()

    result, summary = diversity_engine.enforce(products, mission_ctx, rec_ctx)
    assert len(result) == 2
    assert summary["drop_reasons"]["brand_limit"] == 1

def test_diversity_category_limit(diversity_engine):
    products = [
        ScoredProduct(product_id="1", name="Prod1", brand="B1", category="C1", price=10.0, score_breakdown=ScoreBreakdown(base_score=1.0)),
        ScoredProduct(product_id="2", name="Prod2", brand="B2", category="C1", price=10.0, score_breakdown=ScoreBreakdown(base_score=1.0)),
        ScoredProduct(product_id="3", name="Prod3", brand="B3", category="C1", price=10.0, score_breakdown=ScoreBreakdown(base_score=1.0)),
        ScoredProduct(product_id="4", name="Prod4", brand="B4", category="C1", price=10.0, score_breakdown=ScoreBreakdown(base_score=1.0)),
    ]
    mission_ctx = get_mission_ctx()
    rec_ctx = RecommendationContext()

    result, summary = diversity_engine.enforce(products, mission_ctx, rec_ctx)
    assert len(result) == 3
    assert summary["drop_reasons"]["category_limit"] == 1

def test_diversity_subcategory_limit(diversity_engine):
    products = [
        ScoredProduct(product_id="1", name="Prod1", brand="B1", category="C1", subcategory="S1", price=10.0, score_breakdown=ScoreBreakdown(base_score=1.0)),
        ScoredProduct(product_id="2", name="Prod2", brand="B2", category="C1", subcategory="S1", price=10.0, score_breakdown=ScoreBreakdown(base_score=1.0)),
    ]
    mission_ctx = get_mission_ctx()
    rec_ctx = RecommendationContext()

    diversity_engine.config["max_per_subcategory"] = 1
    result, summary = diversity_engine.enforce(products, mission_ctx, rec_ctx)
    assert len(result) == 1
    assert summary["drop_reasons"]["subcategory_limit"] == 1

def test_diversity_max_total(diversity_engine):
    products = [
        ScoredProduct(product_id=str(i), name=f"Prod{i}", brand=f"B{i}", category=f"C{i}", price=10.0, score_breakdown=ScoreBreakdown(base_score=1.0))
        for i in range(15)
    ]
    mission_ctx = get_mission_ctx()
    rec_ctx = RecommendationContext()

    result, summary = diversity_engine.enforce(products, mission_ctx, rec_ctx)
    assert len(result) == 10
