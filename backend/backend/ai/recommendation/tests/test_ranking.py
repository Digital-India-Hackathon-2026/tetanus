import math
import json
import os
import pytest
from backend.ai.recommendation.models import CandidateProduct, RecommendationContext
from backend.ai.mission.mission_models import MissionContext, MissionMetadata
from backend.ai.recommendation.ranking.scoring_rules import (
    MissionMatchScorer, BudgetScorer, QualityScorer, RatingScorer,
    ReviewScorer, BrandScorer, CategoryPriorityScorer, BoostEngine, PenaltyEngine
)
from backend.ai.recommendation.ranking.ranking_engine import RankingEngine


@pytest.fixture
def config():
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "ranking", "ranking_config.json"
    )
    with open(config_path) as f:
        full = json.load(f)
    cfg = full["profiles"]["balanced"]
    cfg["thresholds"] = full["thresholds"]
    return cfg


@pytest.fixture
def mission():
    meta = MissionMetadata(aikb_version="1.0", schema_version="1.0", generated_at="2026",
                           mission_hash="x", source="test", loaded_from="test", load_time_ms=1.0)
    return MissionContext(
        mission="Laptop for College",
        supported=True, definition={},
        primary_categories=["Laptops"],
        secondary_categories=["Accessories"],
        required_categories=[], optional_categories=[],
        category_weights={"Laptops": 1.0, "Accessories": 0.5},
        bundle_ids=[], priority="P1", mission_type="hardware", metadata=meta
    )


@pytest.fixture
def rec_ctx():
    return RecommendationContext(budget=1000.0, preferred_brands=["Dell"])


def make_product(**kwargs):
    defaults = dict(product_id="P1", name="Test", category="Laptops", brand="Dell",
                    price=800.0, rating=4.5, review_count=200, quality_score=8.0)
    defaults.update(kwargs)
    return CandidateProduct(**defaults)


# ── MissionMatchScorer ──────────────────────────────────────────────────────

def test_mission_match_primary_category(config, mission, rec_ctx):
    p = make_product(category="Laptops")
    result = MissionMatchScorer().score(p, mission, rec_ctx, config)
    assert result.raw_score == 1.0


def test_mission_match_secondary_category(config, mission, rec_ctx):
    p = make_product(category="Accessories")
    result = MissionMatchScorer().score(p, mission, rec_ctx, config)
    assert result.raw_score == 0.65


def test_mission_match_no_category(config, mission, rec_ctx):
    p = make_product(category="Clothing")
    result = MissionMatchScorer().score(p, mission, rec_ctx, config)
    assert result.raw_score == 0.0


# ── BudgetScorer ─────────────────────────────────────────────────────────────

def test_budget_perfect_match(config, mission, rec_ctx):
    p = make_product(price=1000.0)
    result = BudgetScorer().score(p, mission, rec_ctx, config)
    assert result.raw_score == 1.0


def test_budget_near_match(config, mission, rec_ctx):
    p = make_product(price=900.0)
    result = BudgetScorer().score(p, mission, rec_ctx, config)
    assert 0.9 < result.raw_score < 1.0


def test_budget_over_budget(config, mission, rec_ctx):
    p = make_product(price=1500.0)
    result = BudgetScorer().score(p, mission, rec_ctx, config)
    assert result.raw_score < 0.5


def test_budget_way_over(config, mission, rec_ctx):
    p = make_product(price=9000.0)
    result = BudgetScorer().score(p, mission, rec_ctx, config)
    assert result.raw_score == 0.0


def test_budget_no_budget(config, mission):
    rc = RecommendationContext(budget=None)
    p = make_product(price=9999.0)
    result = BudgetScorer().score(p, mission, rc, config)
    assert result.raw_score == 0.5


# ── QualityScorer ─────────────────────────────────────────────────────────────

def test_quality_normalization(config, mission, rec_ctx):
    p = make_product(quality_score=10.0)
    assert QualityScorer().score(p, mission, rec_ctx, config).raw_score == 1.0
    p = make_product(quality_score=5.0)
    assert QualityScorer().score(p, mission, rec_ctx, config).raw_score == 0.5
    p = make_product(quality_score=0.0)
    assert QualityScorer().score(p, mission, rec_ctx, config).raw_score == 0.0


def test_quality_none(config, mission, rec_ctx):
    p = make_product(quality_score=None)
    assert QualityScorer().score(p, mission, rec_ctx, config).raw_score == 0.5


# ── RatingScorer ─────────────────────────────────────────────────────────────

def test_rating_normalization(config, mission, rec_ctx):
    p = make_product(rating=5.0)
    assert RatingScorer().score(p, mission, rec_ctx, config).raw_score == 1.0
    p = make_product(rating=2.5)
    assert RatingScorer().score(p, mission, rec_ctx, config).raw_score == 0.5
    p = make_product(rating=0.0)
    assert RatingScorer().score(p, mission, rec_ctx, config).raw_score == 0.0


def test_rating_none(config, mission, rec_ctx):
    p = make_product(rating=None)
    assert RatingScorer().score(p, mission, rec_ctx, config).raw_score == 0.5


# ── ReviewScorer ─────────────────────────────────────────────────────────────

def test_review_log_saturation(config, mission, rec_ctx):
    p_many = make_product(review_count=100)
    p_fewer = make_product(review_count=10)
    r_many = ReviewScorer().score(p_many, mission, rec_ctx, config).raw_score
    r_fewer = ReviewScorer().score(p_fewer, mission, rec_ctx, config).raw_score
    assert r_many > r_fewer
    assert r_many <= 1.0


def test_review_zero(config, mission, rec_ctx):
    p = make_product(review_count=0)
    assert ReviewScorer().score(p, mission, rec_ctx, config).raw_score == 0.0


# ── BrandScorer ───────────────────────────────────────────────────────────────

def test_brand_preferred(config, mission, rec_ctx):
    p = make_product(brand="Dell")
    assert BrandScorer().score(p, mission, rec_ctx, config).raw_score == 1.0


def test_brand_not_preferred(config, mission, rec_ctx):
    p = make_product(brand="HP")
    assert BrandScorer().score(p, mission, rec_ctx, config).raw_score == 0.0


def test_brand_no_preference(config, mission):
    rc = RecommendationContext(budget=1000.0, preferred_brands=[])
    p = make_product(brand="Any")
    assert BrandScorer().score(p, mission, rc, config).raw_score == 0.5


# ── Boost/Penalty ──────────────────────────────────────────────────────────

def test_boost_applied(config, mission, rec_ctx):
    p = make_product(brand="Dell", category="Laptops")
    score, boosts = BoostEngine().apply(0.6, p, mission, rec_ctx, config)
    assert score > 0.6
    assert len(boosts) >= 1


def test_penalty_low_rating(config, mission, rec_ctx):
    p = make_product(rating=1.5, quality_score=8.0)
    score, penalties = PenaltyEngine().apply(0.7, p, config)
    assert score < 0.7
    names = [pen.penalty_name for pen in penalties]
    assert "low_rating" in names


def test_penalty_missing_description(config, mission, rec_ctx):
    p = make_product(description=None)
    score, penalties = PenaltyEngine().apply(0.7, p, config)
    names = [pen.penalty_name for pen in penalties]
    assert "missing_description" in names


# ── RankingEngine ──────────────────────────────────────────────────────────

def test_ranking_engine_sorts_descending(mission, rec_ctx):
    engine = RankingEngine()
    products = [
        make_product(product_id="A", price=1000.0, rating=5.0, quality_score=10.0, brand="Dell", category="Laptops", review_count=500),
        make_product(product_id="B", price=200.0, rating=1.0, quality_score=1.0, brand="Unknown", category="Clothing", review_count=0),
    ]
    scored, report = engine.rank(products, mission, rec_ctx)
    assert scored[0].product_id == "A"
    assert scored[0].final_score > scored[1].final_score


def test_ranking_engine_empty_input(mission, rec_ctx):
    engine = RankingEngine()
    scored, report = engine.rank([], mission, rec_ctx)
    assert scored == []
    assert report.products_ranked == 0


def test_ranking_does_not_mutate_products(mission, rec_ctx):
    engine = RankingEngine()
    original = make_product(price=800.0, quality_score=8.0)
    original_price = original.price
    original_qs = original.quality_score
    engine.rank([original], mission, rec_ctx)
    assert original.price == original_price
    assert original.quality_score == original_qs


def test_ranking_profile_selection(mission, rec_ctx):
    engine_budget = RankingEngine(profile="budget_first")
    engine_quality = RankingEngine(profile="quality_first")
    assert engine_budget.profile == "budget_first"
    assert engine_quality.profile == "quality_first"


def test_ranking_tie_case(mission, rec_ctx):
    engine = RankingEngine()
    products = [
        make_product(product_id="T1", price=1000.0, rating=4.5, quality_score=8.0, brand="Dell", category="Laptops", review_count=200),
        make_product(product_id="T2", price=1000.0, rating=4.5, quality_score=8.0, brand="Dell", category="Laptops", review_count=200),
    ]
    scored, report = engine.rank(products, mission, rec_ctx)
    assert scored[0].final_score == scored[1].final_score
