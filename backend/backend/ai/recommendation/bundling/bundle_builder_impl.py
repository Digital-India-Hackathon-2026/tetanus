import json
import os
from typing import List, Dict, Any
from backend.ai.recommendation.ranking.ranking_models import ScoredProduct
from backend.ai.recommendation.models import RecommendedBundle, RecommendedProduct, RecommendationContext
from backend.ai.mission.mission_models import MissionContext
from backend.ai.mission.mission_loader import MissionLoader


class BundleBuilder:
    """
    Builds product bundles based on AIKB bundle definitions.
    Matches scored products to bundle category slots deterministically.
    """

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "bundle_config.json")
        with open(config_path) as f:
            self.config = json.load(f)
        loader = MissionLoader()
        self._bundle_knowledge = loader.load_bundles() or {}

    def _estimate_missing_cost(self, missing_items: List[str], graph_repo) -> float:
        """Estimates cost of missing items by querying Neo4j for median/minimum prices."""
        from backend.ai.recommendation.config import RecommendationConfig
        config = RecommendationConfig()
        default_price = config.default_fallback_price
        
        if not graph_repo or not hasattr(graph_repo, "driver"):
            return len(missing_items) * default_price
            
        total_cost = 0.0
        try:
            with graph_repo.driver.session() as session:
                for item in missing_items:
                    # Try to find products that match the missing item name or category
                    query = """
                    MATCH (p:Product)
                    WHERE toLower(p.name) CONTAINS toLower($item) 
                       OR toLower(p.category) CONTAINS toLower($item)
                       OR toLower(p.subcategory) CONTAINS toLower($item)
                    RETURN p.price AS price
                    ORDER BY p.price ASC
                    LIMIT 5
                    """
                    result = session.run(query, item=item)
                    prices = [record["price"] for record in result if record["price"] is not None]
                    if prices:
                        # Use median of bottom 5 prices to be realistic but not skewed by outliers
                        prices.sort()
                        median_price = prices[len(prices)//2]
                        total_cost += float(median_price)
                    else:
                        total_cost += default_price
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Failed to estimate missing cost: {e}")
            total_cost += len(missing_items) * default_price
            
        return total_cost

    def build_bundles(
        self,
        scored_products: List[ScoredProduct],
        mission_context: MissionContext,
        recommendation_context: RecommendationContext,
        graph_repo=None
    ) -> List[RecommendedBundle]:
        from backend.ai.knowledge.mission_profiles import get_mission_profile
        
        max_bundles = self.config.get("max_bundles", 2)
        min_bundle_size = self.config.get("min_bundle_size", 2)
        max_bundle_size = self.config.get("max_bundle_size", 4)

        if not mission_context.bundle_ids:
            return []
            
        mission_profile = get_mission_profile(mission_context.mission)
        essential_items = mission_profile.get("essential", [])
        optional_items = mission_profile.get("optional", [])

        # Index products by category
        product_by_category: Dict[str, List[ScoredProduct]] = {}
        for sp in scored_products:
            cat = (sp.category or "other").lower()
            product_by_category.setdefault(cat, []).append(sp)

        bundles: List[RecommendedBundle] = []

        for bundle_id in mission_context.bundle_ids[:max_bundles]:
            # self._bundle_knowledge is a list of dicts
            bundle_def = next((b for b in self._bundle_knowledge if b.get("bundle_name") == bundle_id), None)
            if not bundle_def:
                continue
                
            bundle_categories = bundle_def.get("categories", []) # Might not exist in current JSON, fallback to manual if needed
            bundle_name = bundle_def.get("bundle_name", bundle_id)

            bundle_products = bundle_def.get("products", [])
            
            bundle_items: List[RecommendedProduct] = []
            total_price = 0.0
            used_product_ids = set()

            if bundle_categories:
                for cat in bundle_categories:
                    candidates = product_by_category.get(cat.lower(), [])
                    for sp in candidates:
                        if sp.product_id not in used_product_ids:
                            bundle_items.append(RecommendedProduct(
                                product=sp,
                                justification=f"Part of '{bundle_name}' bundle ({cat})"
                            ))
                            total_price += sp.price
                            used_product_ids.add(sp.product_id)
                            break

                    if len(bundle_items) >= max_bundle_size:
                        break
            elif bundle_products:
                # Match by exact product names if present
                for prod_name in bundle_products:
                    for sp in scored_products:
                        if sp.name == prod_name and sp.product_id not in used_product_ids:
                            bundle_items.append(RecommendedProduct(
                                product=sp,
                                justification=f"Part of '{bundle_name}' bundle"
                            ))
                            total_price += sp.price
                            used_product_ids.add(sp.product_id)
                            break
                    if len(bundle_items) >= max_bundle_size:
                        break
            if not bundle_items:
                # Fallback: Just bundle the top N diverse products
                for sp in scored_products:
                    if sp.product_id not in used_product_ids:
                        bundle_items.append(RecommendedProduct(
                            product=sp,
                            justification=f"Top choice for '{bundle_name}'"
                        ))
                        total_price += sp.price
                        used_product_ids.add(sp.product_id)
                    if len(bundle_items) >= max_bundle_size:
                        break

            if len(bundle_items) >= min_bundle_size:
                # Calculate basic metrics
                required_count = len(bundle_categories) if bundle_categories else len(bundle_products)
                found_count = len(bundle_items)
                completeness = found_count / required_count if required_count > 0 else 1.0

                found_categories = {rp.product.category.lower() for rp in bundle_items if rp.product.category}
                missing_categories = [c for c in bundle_categories if c.lower() not in found_categories]

                found_products = {rp.product.name.lower() for rp in bundle_items}
                missing_products = [p for p in bundle_products if p.lower() not in found_products]
                
                budget = recommendation_context.budget
                budget_utilization = total_price / budget if budget and budget > 0 else 0.0
                
                # --- New Readiness Metrics ---
                essential_found = []
                essential_missing = []
                optional_found = []
                optional_missing = []
                
                # Helper to check if an item text is found in bundle products
                def is_item_in_bundle(item: str) -> bool:
                    for rp in bundle_items:
                        ptxt = f"{rp.product.name} {rp.product.description or ''} {rp.product.category or ''}".lower()
                        if item.lower() in ptxt:
                            return True
                    return False
                
                for item in essential_items:
                    if is_item_in_bundle(item):
                        essential_found.append(item)
                    else:
                        essential_missing.append(item)
                        
                for item in optional_items:
                    if is_item_in_bundle(item):
                        optional_found.append(item)
                    else:
                        optional_missing.append(item)
                        
                total_essentials = len(essential_items)
                completion_percentage = (len(essential_found) / total_essentials) if total_essentials > 0 else 1.0
                
                # Readiness score (weighted blend: 70% essentials, 30% optionals)
                total_optionals = len(optional_items)
                opt_completion = (len(optional_found) / total_optionals) if total_optionals > 0 else 1.0
                readiness_score = (completion_percentage * 0.7) + (opt_completion * 0.3)
                
                # Estimate remaining cost
                estimated_remaining_cost = self._estimate_missing_cost(essential_missing, graph_repo)

                bundles.append(RecommendedBundle(
                    bundle_id=bundle_id,
                    name=bundle_name,
                    products=bundle_items,
                    total_price=total_price,
                    bundle_score=sum(rp.product.final_score for rp in bundle_items) / found_count if found_count > 0 else 0.0,
                    completeness=completeness,
                    missing_categories=missing_categories,
                    missing_products=missing_products,
                    budget_utilization=budget_utilization,
                    readiness_score=readiness_score,
                    essential_items_found=essential_found,
                    essential_items_missing=essential_missing,
                    optional_items_found=optional_found,
                    optional_items_missing=optional_missing,
                    completion_percentage=completion_percentage,
                    estimated_remaining_cost=estimated_remaining_cost
                ))

        return bundles
