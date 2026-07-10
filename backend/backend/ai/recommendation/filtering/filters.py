import json
import os
import time
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, Type

from backend.ai.recommendation.models import CandidateProduct, RecommendationContext
from backend.ai.mission.mission_models import MissionContext
from backend.ai.recommendation.filtering.filter_models import FilterDecision, PerFilterTelemetry, FilterReport

class BaseFilter(ABC):
    @abstractmethod
    def apply(
        self, 
        products: List[CandidateProduct], 
        mission_context: MissionContext, 
        recommendation_context: RecommendationContext,
        config: Dict[str, Any]
    ) -> Tuple[List[CandidateProduct], List[FilterDecision]]:
        pass

class FilterRegistry:
    _filters: Dict[str, Type[BaseFilter]] = {}

    @classmethod
    def register(cls, name: str):
        def wrapper(filter_class: Type[BaseFilter]):
            cls._filters[name] = filter_class
            return filter_class
        return wrapper

    @classmethod
    def get_filter(cls, name: str) -> BaseFilter:
        if name not in cls._filters:
            raise ValueError(f"Filter {name} not found in registry")
        return cls._filters[name]()

@FilterRegistry.register("BudgetFilter")
class BudgetFilter(BaseFilter):
    def apply(self, products, mission_context, recommendation_context, config):
        kept = []
        decisions = []
        
        budget = recommendation_context.budget
        if budget is None:
            return products, []

        multiplier = config.get("max_budget_multiplier", 1.0)
        max_allowed = budget * multiplier

        for p in products:
            if p.price > max_allowed:
                decisions.append(FilterDecision(
                    filter_name="BudgetFilter",
                    product_id=p.product_id,
                    product_name=p.name,
                    reason=f"Price {p.price} exceeds max allowed {max_allowed}",
                    metadata={"price": p.price, "max_allowed": max_allowed}
                ))
            else:
                kept.append(p)
        
        return kept, decisions

@FilterRegistry.register("MissionCategoryFilter")
class MissionCategoryFilter(BaseFilter):
    def apply(self, products, mission_context, recommendation_context, config):
        kept = []
        decisions = []
        
        allowed_categories = set(mission_context.primary_categories + mission_context.secondary_categories)
        
        for p in products:
            if p.category not in allowed_categories:
                decisions.append(FilterDecision(
                    filter_name="MissionCategoryFilter",
                    product_id=p.product_id,
                    product_name=p.name,
                    reason=f"Category '{p.category}' not in allowed mission categories",
                    metadata={"category": p.category, "allowed": list(allowed_categories)}
                ))
            else:
                kept.append(p)
        return kept, decisions

@FilterRegistry.register("BrandFilter")
class BrandFilter(BaseFilter):
    def apply(self, products, mission_context, recommendation_context, config):
        kept = []
        decisions = []
        
        pref = set(recommendation_context.preferred_brands) if recommendation_context.preferred_brands else set()
        excl = set(recommendation_context.excluded_brands) if recommendation_context.excluded_brands else set()

        for p in products:
            if pref and p.brand not in pref:
                decisions.append(FilterDecision(
                    filter_name="BrandFilter",
                    product_id=p.product_id,
                    product_name=p.name,
                    reason=f"Brand '{p.brand}' not in preferred brands",
                    metadata={"brand": p.brand, "preferred": list(pref)}
                ))
            elif p.brand in excl:
                decisions.append(FilterDecision(
                    filter_name="BrandFilter",
                    product_id=p.product_id,
                    product_name=p.name,
                    reason=f"Brand '{p.brand}' is excluded",
                    metadata={"brand": p.brand, "excluded": list(excl)}
                ))
            else:
                kept.append(p)
                
        return kept, decisions

@FilterRegistry.register("InventoryFilter")
class InventoryFilter(BaseFilter):
    def apply(self, products, mission_context, recommendation_context, config):
        kept = []
        decisions = []
        
        allow_oos = config.get("allow_out_of_stock", False)
        
        for p in products:
            # Placeholder: no DB check yet, assume all have inventory unless explicitly 0
            if not allow_oos and p.inventory is not None and p.inventory <= 0:
                decisions.append(FilterDecision(
                    filter_name="InventoryFilter",
                    product_id=p.product_id,
                    product_name=p.name,
                    reason="Product is out of stock",
                    metadata={"inventory": p.inventory}
                ))
            else:
                kept.append(p)
        return kept, decisions

@FilterRegistry.register("QualityFilter")
class QualityFilter(BaseFilter):
    def apply(self, products, mission_context, recommendation_context, config):
        kept = []
        decisions = []
        
        min_quality = config.get("minimum_quality_score", 0.0)
        
        for p in products:
            if p.quality_score is not None and p.quality_score < min_quality:
                decisions.append(FilterDecision(
                    filter_name="QualityFilter",
                    product_id=p.product_id,
                    product_name=p.name,
                    reason=f"Quality score {p.quality_score} below minimum {min_quality}",
                    metadata={"quality_score": p.quality_score, "min_quality": min_quality}
                ))
            else:
                kept.append(p)
        return kept, decisions

@FilterRegistry.register("DuplicateFilter")
class DuplicateFilter(BaseFilter):
    def apply(self, products, mission_context, recommendation_context, config):
        kept = []
        decisions = []
        
        if not config.get("remove_duplicates", True):
            return products, []

        seen_ids = set()
        seen_names = set()
        
        best_versions = {}
        for p in products:
            key = p.name.lower()
            if key not in best_versions:
                best_versions[key] = p
            else:
                existing = best_versions[key]
                eq = (existing.quality_score or 0)
                nq = (p.quality_score or 0)
                if nq > eq:
                    decisions.append(FilterDecision(
                        filter_name="DuplicateFilter",
                        product_id=existing.product_id,
                        product_name=existing.name,
                        reason="Duplicate found, keeping higher quality version",
                        metadata={"kept_id": p.product_id}
                    ))
                    best_versions[key] = p
                else:
                    decisions.append(FilterDecision(
                        filter_name="DuplicateFilter",
                        product_id=p.product_id,
                        product_name=p.name,
                        reason="Duplicate found, keeping higher quality version",
                        metadata={"kept_id": existing.product_id}
                    ))
        
        for p in best_versions.values():
            if p.product_id not in seen_ids:
                seen_ids.add(p.product_id)
                kept.append(p)
            else:
                decisions.append(FilterDecision(
                    filter_name="DuplicateFilter",
                    product_id=p.product_id,
                    product_name=p.name,
                    reason="Duplicate product ID",
                    metadata={}
                ))
        
        # Preserve original order
        final_kept = [p for p in products if p in kept]
        return final_kept, decisions

class FilterPipeline:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "filter_config.json")
            
        with open(config_path, "r") as f:
            self.config = json.load(f)
            
        self.filter_order = self.config.get("filter_order", [])

    def run(
        self, 
        products: List[CandidateProduct], 
        mission_context: MissionContext, 
        recommendation_context: RecommendationContext
    ) -> Tuple[List[CandidateProduct], FilterReport]:
        
        start_time = time.time()
        report = FilterReport(input_products=len(products))
        
        current_products = products
        
        for filter_name in self.filter_order:
            filter_start = time.time()
            products_in = len(current_products)
            
            try:
                filter_instance = FilterRegistry.get_filter(filter_name)
                current_products, decisions = filter_instance.apply(
                    current_products, mission_context, recommendation_context, self.config
                )
                report.decisions.extend(decisions)
            except ValueError as e:
                print(f"Warning: {e}")
                
            filter_end = time.time()
            report.telemetry.append(PerFilterTelemetry(
                filter_name=filter_name,
                execution_time_ms=(filter_end - filter_start) * 1000,
                products_in=products_in,
                products_out=len(current_products)
            ))
            
        report.remaining_products = len(current_products)
        report.execution_time_ms = (time.time() - start_time) * 1000
        
        return current_products, report
