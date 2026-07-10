import logging
from typing import List, Optional
from backend.ai.gemini import GeminiClient
from backend.ai.recommendation.ranking.ranking_models import ScoredProduct
from backend.ai.recommendation.models import RecommendationContext, RecommendedBundle
from backend.ai.mission.mission_models import MissionContext

logger = logging.getLogger("CIN.ExplanationAgent")


class ExplanationAgent:
    """
    Generates natural language explanations for recommendations using Gemini.
    Falls back to template-based explanations if Gemini fails.
    """

    def __init__(self, gemini_client: Optional[GeminiClient] = None):
        self.gemini = gemini_client or GeminiClient()

    async def generate_explanation_async(
        self,
        query: str,
        mission_context: MissionContext,
        recommendation_context: RecommendationContext,
        top_products: List[ScoredProduct],
        bundles: Optional[List[RecommendedBundle]] = None,
    ) -> str:
        if not top_products:
            return "I couldn't find products matching your requirements. Please try refining your search."
        try:
            return await self._gemini_explanation(query, mission_context, recommendation_context, top_products, bundles)
        except Exception as e:
            logger.warning(f"Gemini explanation failed ({e}), using template fallback")
            return self._template_explanation(top_products, mission_context, bundles)

    def generate_explanation(
        self,
        query: str,
        mission_context: MissionContext,
        recommendation_context: RecommendationContext,
        top_products: List[ScoredProduct],
        bundles: Optional[List[RecommendedBundle]] = None,
    ) -> str:
        """Synchronous fallback — always uses template (no Gemini call)."""
        if not top_products:
            return "I couldn't find products matching your requirements. Please try refining your search."
        return self._template_explanation(top_products, mission_context, bundles)

    async def _gemini_explanation(self, query, mission_context, recommendation_context, top_products, bundles):
        products_text = ""
        for i, sp in enumerate(top_products[:3], 1):
            reasons = " | ".join(sp.score_breakdown.top_reasons[:3]) if sp.score_breakdown.top_reasons else "Strong match"
            products_text += f"{i}. {sp.name} (Brand: {sp.brand}, Price: Rs.{sp.price:.0f}, Score: {sp.final_score:.2f})\n   Reasons: {reasons}\n\n"

        budget_str = f"Rs.{recommendation_context.budget:.0f}" if recommendation_context.budget else "flexible"
        bundle_hint = ""
        if bundles:
            b = bundles[0]
            bundle_hint = f"\n\nA bundle '{b.name}' is also available at Rs.{b.total_price:.0f}.\n"
            bundle_hint += f"Readiness Score: {b.readiness_score:.2f}\n"
            if b.essential_items_missing:
                bundle_hint += f"Missing essentials: {', '.join(b.essential_items_missing)}\n"
                bundle_hint += f"Estimated remaining cost: Rs.{b.estimated_remaining_cost:.0f}\n"
            else:
                bundle_hint += "All essentials included!\n"

        prompt = f"""You are a helpful product recommendation assistant for an Indian e-commerce platform.

Customer query: "{query}"
Mission: {mission_context.mission}
Budget: {budget_str}

Top recommended products:
{products_text}{bundle_hint}
Write a SHORT, friendly recommendation (3-4 sentences). Acknowledge their need, highlight the top 1-2 products with specific reasons, mention price. Keep it conversational, no bullet points. If a bundle is present, briefly summarize its readiness and missing essentials without hallucinating. Do NOT mention readiness score numbers directly."""

        import hashlib
        cache_key = hashlib.md5(f"{mission_context.mission}_{budget_str}_{','.join([sp.product_id for sp in top_products[:3]])}_v1".encode()).hexdigest()

        response = await self.gemini.generate_content(
            prompt=prompt,
            temperature=0.4,
            max_tokens=300,
            cache_key=cache_key,
            fallback_text=self._template_explanation(top_products, mission_context, bundles)
        )
        return response.text.strip() if response and response.text else self._template_explanation(top_products, mission_context, bundles)

    def _template_explanation(self, top_products, mission_context, bundles):
        top = top_products[0]
        reasons = " and ".join(top.score_breakdown.top_reasons[:2]) if top.score_breakdown.top_reasons else "it's a strong match for your needs"
        text = (
            f"Based on your search for '{mission_context.mission}', I recommend the {top.name} by {top.brand} "
            f"at Rs.{top.price:.0f}. It stands out because {reasons}. "
        )
        if len(top_products) > 1:
            second = top_products[1]
            text += f"The {second.name} at Rs.{second.price:.0f} is also a great option."
        if bundles:
            text += f" Check out the '{bundles[0].name}' bundle for a complete setup at Rs.{bundles[0].total_price:.0f}."
        return text
