import pytest
import os
import json
from backend.ai.recommendation.models import CandidateProduct, RecommendationContext
from backend.ai.mission.mission_models import MissionContext, MissionMetadata
from backend.ai.recommendation.filtering.filters import FilterPipeline

@pytest.fixture
def mock_config(tmp_path):
    config = {
        "allow_out_of_stock": False,
        "max_budget_multiplier": 1.2,
        "minimum_rating": 0,
        "minimum_quality_score": 5.0,
        "remove_duplicates": True,
        "filter_order": [
            "BudgetFilter",
            "MissionCategoryFilter",
            "BrandFilter",
            "InventoryFilter",
            "QualityFilter",
            "DuplicateFilter"
        ]
    }
    config_path = tmp_path / "filter_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f)
    return str(config_path)

@pytest.fixture
def base_mission_context():
    meta = MissionMetadata(
        aikb_version="1.0",
        schema_version="1.0",
        generated_at="2026",
        mission_hash="abc",
        source="test",
        loaded_from="test",
        load_time_ms=1.0
    )
    return MissionContext(
        mission="Test Mission",
        supported=True,
        definition={},
        primary_categories=["Electronics"],
        secondary_categories=["Accessories"],
        required_categories=[],
        optional_categories=[],
        category_weights={},
        bundle_ids=[],
        priority="P1",
        mission_type="test",
        metadata=meta
    )

@pytest.fixture
def base_recommendation_context():
    return RecommendationContext(
        budget=1000.0,
        preferred_brands=[],
        excluded_brands=[]
    )

@pytest.fixture
def candidate_products():
    return [
        CandidateProduct(product_id="1", name="Laptop", category="Electronics", brand="Dell", price=800.0, inventory=10, quality_score=8.0),
        CandidateProduct(product_id="2", name="Phone", category="Electronics", brand="Apple", price=1500.0, inventory=5, quality_score=9.0),
        CandidateProduct(product_id="3", name="Shirt", category="Clothing", brand="Nike", price=50.0, inventory=100, quality_score=7.0),
        CandidateProduct(product_id="4", name="Mouse", category="Accessories", brand="Logitech", price=25.0, inventory=0, quality_score=6.0),
        CandidateProduct(product_id="5", name="Cheap Laptop", category="Electronics", brand="Dell", price=500.0, inventory=2, quality_score=3.0),
        CandidateProduct(product_id="6", name="Laptop", category="Electronics", brand="Dell", price=800.0, inventory=10, quality_score=9.0), # duplicate of 1, but better quality
    ]

def test_filtering_pipeline(mock_config, base_mission_context, base_recommendation_context, candidate_products):
    pipeline = FilterPipeline(config_path=mock_config)
    
    filtered, report = pipeline.run(candidate_products, base_mission_context, base_recommendation_context)
    
    # 1: Laptop (800) -> kept initially, but duplicate 6 has better quality. Wait, ID is different ("1" vs "6"), but name "Laptop" is same. DuplicateFilter removes 1 in favor of 6.
    # 2: Phone (1500) -> Budget is 1000 * 1.2 = 1200. Fails budget.
    # 3: Shirt (50) -> Category 'Clothing' not in Mission (Electronics, Accessories). Fails category.
    # 4: Mouse (25) -> Inventory is 0. config allow_out_of_stock is False. Fails inventory.
    # 5: Cheap Laptop (500) -> Quality 3.0 < 5.0. Fails quality.
    # 6: Laptop (800) -> Kept.
    
    assert len(filtered) == 1
    assert filtered[0].product_id == "6"
    assert report.input_products == 6
    assert report.remaining_products == 1
    
    reasons = {d.product_id: d.filter_name for d in report.decisions}
    assert "2" in reasons and reasons["2"] == "BudgetFilter"
    assert "3" in reasons and reasons["3"] == "MissionCategoryFilter"
    assert "4" in reasons and reasons["4"] == "InventoryFilter"
    assert "5" in reasons and reasons["5"] == "QualityFilter"
    assert "1" in reasons and reasons["1"] == "DuplicateFilter"

def test_filtering_brands(mock_config, base_mission_context, base_recommendation_context):
    pipeline = FilterPipeline(config_path=mock_config)
    
    base_recommendation_context.budget = 5000.0 # prevent budget failure
    base_recommendation_context.preferred_brands = ["Dell"]
    
    products = [
        CandidateProduct(product_id="1", name="P1", category="Electronics", brand="Dell", price=800.0, inventory=10, quality_score=8.0),
        CandidateProduct(product_id="2", name="P2", category="Electronics", brand="HP", price=800.0, inventory=10, quality_score=8.0),
    ]
    
    filtered, report = pipeline.run(products, base_mission_context, base_recommendation_context)
    assert len(filtered) == 1
    assert filtered[0].product_id == "1"

    # Test excluded brands
    base_recommendation_context.preferred_brands = []
    base_recommendation_context.excluded_brands = ["Dell"]
    filtered, report = pipeline.run(products, base_mission_context, base_recommendation_context)
    assert len(filtered) == 1
    assert filtered[0].product_id == "2"

def test_filtering_empty_list(mock_config, base_mission_context, base_recommendation_context):
    pipeline = FilterPipeline(config_path=mock_config)
    filtered, report = pipeline.run([], base_mission_context, base_recommendation_context)
    assert len(filtered) == 0
    assert report.input_products == 0
    assert report.remaining_products == 0

def test_filtering_no_budget(mock_config, base_mission_context, base_recommendation_context):
    pipeline = FilterPipeline(config_path=mock_config)
    base_recommendation_context.budget = None
    
    products = [
        CandidateProduct(product_id="1", name="Expensive", category="Electronics", brand="Dell", price=99999.0, inventory=10, quality_score=8.0),
    ]
    filtered, report = pipeline.run(products, base_mission_context, base_recommendation_context)
    assert len(filtered) == 1
