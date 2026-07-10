import json
import os
from typing import List, Dict, Any
from backend.ai.recommendation.ranking.ranking_models import ScoredProduct
from backend.ai.mission.mission_models import MissionContext
from backend.ai.recommendation.models import RecommendationContext


class DiversityEngine:
    """
    Enforces diversity by capping the number of products per brand and category.
    Preserves score order within each group.
    """

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "diversity_config.json")
        with open(config_path) as f:
            self.config = json.load(f)

    def enforce(
        self,
        scored_products: List[ScoredProduct],
        mission_context: MissionContext,
        recommendation_context: RecommendationContext,
    ) -> tuple[List[ScoredProduct], Dict[str, Any]]:
        max_per_brand = self.config.get("max_per_brand", 2)
        max_per_category = self.config.get("max_per_category", 3)
        max_per_subcategory = self.config.get("max_per_subcategory", 2)
        max_total = self.config.get("max_total_results", 10)

        brand_counts: Dict[str, int] = {}
        category_counts: Dict[str, int] = {}
        subcategory_counts: Dict[str, int] = {}
        seen_names = set()
        
        result: List[ScoredProduct] = []
        dropped_count = 0
        reasons: Dict[str, int] = {"brand_limit": 0, "category_limit": 0, "subcategory_limit": 0, "duplicate": 0}

        for sp in scored_products:
            if len(result) >= max_total:
                break
                
            brand = (sp.brand or "unknown").lower()
            category = (sp.category or "unknown").lower()
            subcategory = (sp.subcategory or "unknown").lower()
            name_lower = sp.name.lower().strip()
            
            if name_lower in seen_names:
                dropped_count += 1
                reasons["duplicate"] += 1
                continue

            if brand != "unknown" and brand_counts.get(brand, 0) >= max_per_brand:
                dropped_count += 1
                reasons["brand_limit"] += 1
                continue
            if category_counts.get(category, 0) >= max_per_category:
                dropped_count += 1
                reasons["category_limit"] += 1
                continue
            if subcategory != "unknown" and subcategory_counts.get(subcategory, 0) >= max_per_subcategory:
                dropped_count += 1
                reasons["subcategory_limit"] += 1
                continue

            brand_counts[brand] = brand_counts.get(brand, 0) + 1
            category_counts[category] = category_counts.get(category, 0) + 1
            subcategory_counts[subcategory] = subcategory_counts.get(subcategory, 0) + 1
            seen_names.add(name_lower)
            result.append(sp)

        summary = {
            "input_count": len(scored_products),
            "output_count": len(result),
            "dropped_count": dropped_count,
            "drop_reasons": reasons
        }
        return result, summary
