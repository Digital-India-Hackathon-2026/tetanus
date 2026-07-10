import math
from abc import ABC, abstractmethod
from typing import Dict, Type, List, Any

from backend.ai.recommendation.models import CandidateProduct, RecommendationContext
from backend.ai.mission.mission_models import MissionContext
from backend.ai.recommendation.ranking.ranking_models import ScoringResult


class ScorerRegistry:
    _scorers: Dict[str, Type["BaseScorer"]] = {}

    @classmethod
    def register(cls, name: str):
        def wrapper(scorer_class: Type["BaseScorer"]):
            cls._scorers[name] = scorer_class
            return scorer_class
        return wrapper

    @classmethod
    def get_scorer(cls, name: str) -> "BaseScorer":
        if name not in cls._scorers:
            raise ValueError(f"Scorer '{name}' not found in registry. Available: {list(cls._scorers.keys())}")
        return cls._scorers[name]()

    @classmethod
    def list_scorers(cls) -> List[str]:
        return list(cls._scorers.keys())


class BaseScorer(ABC):
    @abstractmethod
    def score(
        self,
        product: CandidateProduct,
        mission_context: MissionContext,
        recommendation_context: RecommendationContext,
        config: Dict[str, Any]
    ) -> ScoringResult:
        """Returns a ScoringResult with raw_score in [0,1], weighted_score, and explanation."""
        pass


@ScorerRegistry.register("mission_match")
class MissionMatchScorer(BaseScorer):
    def score(self, product, mission_context, recommendation_context, config) -> ScoringResult:
        weight = config["weights"].get("mission_match", 0.0)
        category = (product.category or "").strip()
        category_weights = mission_context.category_weights or {}

        if category in mission_context.primary_categories:
            raw = 1.0
            explanation = f"Product category '{category}' is a primary mission category"
        elif category in mission_context.secondary_categories:
            raw = 0.65
            explanation = f"Product category '{category}' is a secondary mission category"
        elif category in category_weights:
            raw = min(category_weights[category], 1.0)
            explanation = f"Product category '{category}' has a mission weight of {raw:.2f}"
        else:
            raw = 0.0
            explanation = f"Product category '{category}' has no mission relevance"

        return ScoringResult(
            scorer_name="MissionMatchScorer",
            raw_score=raw,
            weighted_score=raw * weight,
            explanation=explanation
        )


@ScorerRegistry.register("budget_match")
class BudgetScorer(BaseScorer):
    def score(self, product, mission_context, recommendation_context, config) -> ScoringResult:
        weight = config["weights"].get("budget_match", 0.0)
        budget = recommendation_context.budget
        tol = config.get("thresholds", {}).get("budget_tolerance_factor", 0.5)

        if budget is None or budget <= 0:
            return ScoringResult(
                scorer_name="BudgetScorer",
                raw_score=0.5,
                weighted_score=0.5 * weight,
                explanation="No budget specified, using neutral score"
            )

        ratio = product.price / budget
        if ratio <= 1.0:
            # Smooth curve: penalize extremely cheap products slightly
            raw = 1.0 - tol * (1.0 - ratio) ** 2
        else:
            # Smooth decay above budget
            over = ratio - 1.0
            raw = max(0.0, 1.0 - (over / tol) ** 2)

        raw = max(0.0, min(1.0, raw))
        explanation = f"Price {product.price} vs budget {budget} (ratio={ratio:.2f})"

        return ScoringResult(
            scorer_name="BudgetScorer",
            raw_score=raw,
            weighted_score=raw * weight,
            explanation=explanation
        )


@ScorerRegistry.register("quality_score")
class QualityScorer(BaseScorer):
    def score(self, product, mission_context, recommendation_context, config) -> ScoringResult:
        weight = config["weights"].get("quality_score", 0.0)
        qs = product.quality_score

        if qs is None:
            raw = 0.5
            explanation = "No quality score available, using neutral"
        else:
            raw = max(0.0, min(1.0, qs / 10.0))
            explanation = f"Quality score {qs}/10 normalized to {raw:.2f}"

        return ScoringResult(
            scorer_name="QualityScorer",
            raw_score=raw,
            weighted_score=raw * weight,
            explanation=explanation
        )


@ScorerRegistry.register("rating")
class RatingScorer(BaseScorer):
    def score(self, product, mission_context, recommendation_context, config) -> ScoringResult:
        weight = config["weights"].get("rating", 0.0)
        rating = product.rating

        if rating is None:
            raw = 0.5
            explanation = "No rating available, using neutral"
        else:
            raw = max(0.0, min(1.0, rating / 5.0))
            explanation = f"Rating {rating}/5 normalized to {raw:.2f}"

        return ScoringResult(
            scorer_name="RatingScorer",
            raw_score=raw,
            weighted_score=raw * weight,
            explanation=explanation
        )


@ScorerRegistry.register("review_count")
class ReviewScorer(BaseScorer):
    def score(self, product, mission_context, recommendation_context, config) -> ScoringResult:
        weight = config["weights"].get("review_count", 0.0)
        count = product.review_count
        log_scale = config.get("thresholds", {}).get("review_log_scale", 100)

        if count is None or count <= 0:
            raw = 0.0
            explanation = "No reviews available"
        else:
            raw = min(1.0, math.log1p(count) / math.log1p(log_scale))
            explanation = f"{count} reviews, log-normalized to {raw:.2f} (scale={log_scale})"

        return ScoringResult(
            scorer_name="ReviewScorer",
            raw_score=raw,
            weighted_score=raw * weight,
            explanation=explanation
        )


@ScorerRegistry.register("brand_preference")
class BrandScorer(BaseScorer):
    def score(self, product, mission_context, recommendation_context, config) -> ScoringResult:
        weight = config["weights"].get("brand_preference", 0.0)
        brand = (product.brand or "").strip()
        preferred = set(recommendation_context.preferred_brands or [])

        if not preferred:
            raw = 0.5
            explanation = "No brand preference specified"
        elif brand in preferred:
            raw = 1.0
            explanation = f"Brand '{brand}' is in preferred brands"
        else:
            raw = 0.0
            explanation = f"Brand '{brand}' is not in preferred brands"

        return ScoringResult(
            scorer_name="BrandScorer",
            raw_score=raw,
            weighted_score=raw * weight,
            explanation=explanation
        )


@ScorerRegistry.register("category_priority")
class CategoryPriorityScorer(BaseScorer):
    def score(self, product, mission_context, recommendation_context, config) -> ScoringResult:
        weight = config["weights"].get("category_priority", 0.0)
        category = (product.category or "").strip()
        category_weights = mission_context.category_weights or {}

        if category in category_weights:
            raw = min(1.0, float(category_weights[category]))
            explanation = f"Category '{category}' has explicit mission weight {raw:.2f}"
        elif category in mission_context.primary_categories:
            raw = 1.0
            explanation = f"Category '{category}' is a primary mission category"
        elif category in mission_context.secondary_categories:
            raw = 0.5
            explanation = f"Category '{category}' is a secondary mission category"
        else:
            raw = 0.0
            explanation = f"Category '{category}' not found in mission context"

        return ScoringResult(
            scorer_name="CategoryPriorityScorer",
            raw_score=raw,
            weighted_score=raw * weight,
            explanation=explanation
        )


@ScorerRegistry.register("intent_bonus")
class IntentBonusScorer(BaseScorer):
    def score(self, product, mission_context, recommendation_context, config) -> ScoringResult:
        weight = config["weights"].get("intent_bonus", 1.0)
        from backend.ai.knowledge.mission_profiles import get_mission_profile
        from backend.ai.recommendation.config import RecommendationConfig
        
        # We need access to the config to get mission-specific bonus.
        # But for now we can instantiate it or fetch it, or just use the config dict passed.
        # The prompt says we can fetch it via mission_profiles
        profile = get_mission_profile(mission_context.mission)
        essentials = profile.get("essential", [])
        
        # Get the configured intent bonus
        rec_config = RecommendationConfig()
        bonus_config = rec_config.intent_bonus_scores.get(mission_context.mission.lower(), {})
        bonus_score = bonus_config.get("bonus", rec_config.default_intent_bonus)
        
        product_text = f"{product.name} {product.description or ''} {product.category or ''} {product.subcategory or ''}".lower()
        
        matched_essential = None
        for essential in essentials:
            if essential.lower() in product_text:
                matched_essential = essential
                break
                
        if matched_essential:
            raw = bonus_score
            explanation = f"Matches essential mission item: '{matched_essential}' (Bonus: +{raw:.2f})"
        else:
            raw = 0.0
            explanation = "Does not match any essential mission items"

        return ScoringResult(
            scorer_name="IntentBonusScorer",
            raw_score=raw,
            weighted_score=raw * weight,  # The intent bonus adds to the final score if configured via weights, or we just let weighted_score handle it.
            explanation=explanation
        )


class BoostEngine:
    def apply(self, base_score: float, product: CandidateProduct,
              mission_context: MissionContext, recommendation_context: RecommendationContext,
              config: Dict[str, Any]) -> tuple:
        from backend.ai.recommendation.ranking.ranking_models import AppliedBoost
        boosts = config.get("boosts", {})
        thresholds = config.get("thresholds", {})
        applied = []
        score = base_score

        if product.brand in (recommendation_context.preferred_brands or []):
            v = boosts.get("preferred_brand", 0.0)
            if v > 0:
                applied.append(AppliedBoost(boost_name="preferred_brand", boost_value=v,
                                            reason=f"Brand '{product.brand}' is preferred"))
                score = min(1.0, score + v)

        if product.category in (mission_context.primary_categories or []):
            v = boosts.get("primary_category", 0.0)
            if v > 0:
                applied.append(AppliedBoost(boost_name="primary_category", boost_value=v,
                                            reason=f"Category '{product.category}' is primary"))
                score = min(1.0, score + v)

        elif product.category in (mission_context.secondary_categories or []):
            v = boosts.get("secondary_category", 0.0)
            if v > 0:
                applied.append(AppliedBoost(boost_name="secondary_category", boost_value=v,
                                            reason=f"Category '{product.category}' is secondary"))
                score = min(1.0, score + v)

        return score, applied


class PenaltyEngine:
    def apply(self, after_boost_score: float, product: CandidateProduct,
              config: Dict[str, Any]) -> tuple:
        from backend.ai.recommendation.ranking.ranking_models import AppliedPenalty
        penalties = config.get("penalties", {})
        thresholds = config.get("thresholds", {})
        applied = []
        score = after_boost_score

        low_rating_t = thresholds.get("low_rating_threshold", 3.0)
        low_quality_t = thresholds.get("low_quality_threshold", 4.0)

        if product.rating is not None and product.rating < low_rating_t:
            v = penalties.get("low_rating", 0.0)
            if v > 0:
                applied.append(AppliedPenalty(penalty_name="low_rating", penalty_value=v,
                                              reason=f"Rating {product.rating} is below threshold {low_rating_t}"))
                score = max(0.0, score - v)

        if product.quality_score is not None and product.quality_score < low_quality_t:
            v = penalties.get("low_quality", 0.0)
            if v > 0:
                applied.append(AppliedPenalty(penalty_name="low_quality", penalty_value=v,
                                              reason=f"Quality {product.quality_score} is below threshold {low_quality_t}"))
                score = max(0.0, score - v)

        if not product.description:
            v = penalties.get("missing_description", 0.0)
            if v > 0:
                applied.append(AppliedPenalty(penalty_name="missing_description", penalty_value=v,
                                              reason="Product has no description"))
                score = max(0.0, score - v)

        return score, applied


class RankingReasonBuilder:
    """Derives the top deterministic recommendation reasons from scorer outputs."""

    def build(self, score_breakdown) -> List[str]:
        reasons = []
        components = sorted(
            score_breakdown.components, key=lambda c: c.weighted_score, reverse=True
        )

        for c in components[:3]:
            if c.raw_score > 0.6:
                reasons.append(c.explanation)

        for boost in score_breakdown.boosts_applied:
            reasons.append(boost.reason)

        return reasons[:5]

@ScorerRegistry.register('intent_bonus')
class IntentBonusScorer(BaseScorer):
    def score(self, product, mission_context, recommendation_context, config) -> ScoringResult:
        from backend.ai.knowledge.mission_profiles import get_mission_profile
        
        weight = config.get('weights', {}).get('intent_bonus', 0.0)
        
        # Determine the dynamic bonus score from config (defaulting to a global weight if needed)
        mission_name = mission_context.mission.lower() if mission_context and mission_context.mission else ''
        bonus_config = config.get('intent_bonus_map', {}).get(mission_name, {})
        bonus_val = bonus_config.get('bonus', weight)
        
        if not mission_name:
            return ScoringResult(scorer_name='IntentBonusScorer', raw_score=0.0, weighted_score=0.0, explanation='No mission context')
            
        profile = get_mission_profile(mission_name)
        essentials = [e.lower() for e in profile.get('essential', [])]
        
        p_name = product.name.lower() if product.name else ''
        p_cat = product.category.lower() if product.category else ''
        
        # Check if product matches any essential item
        matched = False
        for essential in essentials:
            if essential in p_name or essential in p_cat:
                matched = True
                break
                
        if matched:
            return ScoringResult(
                scorer_name='IntentBonusScorer',
                raw_score=1.0,
                weighted_score=bonus_val,
                explanation=f'Matches essential intent item for mission: {mission_context.mission}'
            )
            
        return ScoringResult(scorer_name='IntentBonusScorer', raw_score=0.0, weighted_score=0.0, explanation='Does not match essential intent items')
