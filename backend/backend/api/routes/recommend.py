import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.ai.agents.intent_agent import IntentAgent
from backend.ai.clarification.clarification_engine import ClarificationEngine
from backend.ai.mission.mission_service import MissionService
from backend.ai.recommendation.recommendation_service import RecommendationService
from backend.ai.recommendation.models import RecommendationContext

logger = logging.getLogger("CIN.API.Recommend")

router = APIRouter()

# Lazy-initialized singletons
_intent_agent: Optional[IntentAgent] = None
_clarification_engine: Optional[ClarificationEngine] = None
_mission_service: Optional[MissionService] = None
_recommendation_service: Optional[RecommendationService] = None


def get_services():
    global _intent_agent, _clarification_engine, _mission_service, _recommendation_service
    if _intent_agent is None:
        _intent_agent = IntentAgent()
        _clarification_engine = ClarificationEngine()
        _mission_service = MissionService()
        _recommendation_service = RecommendationService()
    return _intent_agent, _clarification_engine, _mission_service, _recommendation_service


# ── Request/Response Models ──────────────────────────────────────────────────

class RecommendRequest(BaseModel):
    query: str = Field(..., description="User's natural language shopping query")
    session_id: Optional[str] = Field(None, description="Session ID for multi-turn conversations")
    clarification_answers: Optional[Dict[str, str]] = Field(
        None, description="Answers to clarification questions (question_id -> answer)"
    )
    profile: Optional[str] = Field("balanced", description="Ranking profile: balanced|budget_first|quality_first|premium")


class ProductSummary(BaseModel):
    product_id: str
    name: str
    brand: Optional[str]
    category: Optional[str]
    price: float
    rating: Optional[float]
    quality_score: Optional[float]
    final_score: float
    justification: str
    image_url: Optional[str] = None
    product_url: Optional[str] = None


class BundleSummary(BaseModel):
    bundle_id: str
    name: str
    total_price: float
    bundle_score: float
    product_count: int
    readiness_score: float = 0.0
    completion_percentage: float = 0.0
    essential_items_missing: List[str] = Field(default_factory=list)
    estimated_remaining_cost: float = 0.0


class RecommendResponse(BaseModel):
    status: str
    mission: str
    query: str
    explanation: str
    products: List[ProductSummary]
    bundles: List[BundleSummary]
    needs_clarification: bool
    clarification_questions: List[Dict[str, Any]]
    pipeline_stats: Dict[str, Any]


# ── Main Recommendation Endpoint ─────────────────────────────────────────────

@router.post("/recommend", response_model=RecommendResponse)
async def recommend(request: RecommendRequest):
    """
    Full end-to-end recommendation pipeline:
    Intent → Clarification → Mission → Retrieval → Filter → Rank → Diversity → Bundle → Explain
    """
    intent_agent, clarification_engine, mission_service, recommendation_service = get_services()

    # ── Step 1: Intent Extraction ────────────────────────────────────────────
    try:
        intent_response = await intent_agent.extract_intent(request.query, session_id=request.session_id)
    except Exception as e:
        logger.error(f"Intent extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Intent extraction failed: {str(e)}")

    # ── Step 2: Clarification Check ──────────────────────────────────────────
    clarification_result = clarification_engine.generate_clarification(intent_response)

    if clarification_result.needs_clarification and not request.clarification_answers:
        return RecommendResponse(
            status="needs_clarification",
            mission=intent_response.primary_mission or "unknown",
            query=request.query,
            explanation="Please answer the following questions to help me find the best products for you.",
            products=[],
            bundles=[],
            needs_clarification=True,
            clarification_questions=[
                {"id": q.id, "question": q.question, "type": q.type, "options": q.options}
                for q in clarification_result.questions
            ],
            pipeline_stats={}
        )

    # ── Step 3: Mission Resolution ───────────────────────────────────────────
    try:
        mission_context = mission_service.resolve(intent_response.model_dump())
    except Exception as e:
        logger.error(f"Mission resolution failed: {e}")
        raise HTTPException(status_code=422, detail=f"Mission not found: {str(e)}")

    # ── Step 4: Build RecommendationContext from IntentResponse ──────────────
    constraints = intent_response.constraints
    budget = intent_response.budget
    recommendation_context = RecommendationContext(
        budget=budget.maximum or budget.amount,
        preferred_brands=constraints.preferred_brands or [],
        excluded_brands=constraints.excluded_brands or [],
        urgency=constraints.urgency.value if hasattr(constraints.urgency, 'value') else str(constraints.urgency),
        preferred_price_range=constraints.preferred_price_range,
        inventory_required=constraints.inventory_required.value if hasattr(constraints.inventory_required, 'value') else "in_stock",
    )

    # Override ranking profile if requested
    if request.profile and request.profile != "balanced":
        from backend.ai.recommendation.ranking.ranking_engine import RankingEngine
        recommendation_service.ranking_engine = RankingEngine(profile=request.profile)

    # ── Step 5: Run Recommendation Pipeline ──────────────────────────────────
    try:
        result = recommendation_service.generate_recommendations(
            query=request.query,
            mission_context=mission_context,
            recommendation_context=recommendation_context,
        )
    except Exception as e:
        logger.error(f"Recommendation pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=f"Recommendation pipeline failed: {str(e)}")

    # ── Step 6: Serialize Response ───────────────────────────────────────────
    products_out = [
        ProductSummary(
            product_id=rp.product.product_id,
            name=rp.product.name,
            brand=rp.product.brand,
            category=rp.product.category,
            price=rp.product.price,
            rating=rp.product.rating,
            quality_score=rp.product.quality_score,
            final_score=rp.product.final_score,
            justification=rp.justification,
            image_url=rp.product.image_url,
            product_url=rp.product.product_url,
        )
        for rp in result.products
    ]

    bundles_out = [
        BundleSummary(
            bundle_id=b.bundle_id,
            name=b.name,
            total_price=b.total_price,
            bundle_score=b.bundle_score,
            product_count=len(b.products),
            readiness_score=b.readiness_score,
            completion_percentage=b.completion_percentage,
            essential_items_missing=b.essential_items_missing,
            estimated_remaining_cost=b.estimated_remaining_cost,
        )
        for b in result.bundles
    ]

    return RecommendResponse(
        status="success",
        mission=result.mission,
        query=request.query,
        explanation=result.explanation.markdown if hasattr(result.explanation, "markdown") else str(result.explanation or ""),
        products=products_out,
        bundles=bundles_out,
        needs_clarification=False,
        clarification_questions=[],
        pipeline_stats={
            "retrieved": result.statistics.retrieved_count,
            "filtered": result.statistics.filtered_count,
            "returned": result.statistics.returned_count,
            "execution_ms": round(result.metadata.execution_time_ms, 2),
            "retrieval_ms": round(result.metadata.repository_time_ms, 2),
            "filter_ms": round(result.metadata.filter_time_ms, 2),
            "ranking_ms": round(result.metadata.ranking_time_ms, 2),
        }
    )


@router.post("/clarify")
async def clarify(request: RecommendRequest):
    """
    Dedicated endpoint just to get clarification questions for a query.
    """
    intent_agent, clarification_engine, _, _ = get_services()
    try:
        intent_response = await intent_agent.extract_intent(request.query, session_id=request.session_id)
    except Exception as e:
        logger.error(f"Intent extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Intent extraction failed: {str(e)}")
        
    clarification_result = clarification_engine.generate_clarification(intent_response)
    
    return {
        "needs_clarification": clarification_result.needs_clarification,
        "questions": [
            {"id": q.id, "question": q.question, "type": q.type, "options": q.options}
            for q in clarification_result.questions
        ]
    }


@router.get("/missions")
async def list_missions():
    """List all supported missions from the AIKB."""
    from backend.ai.mission.cache import MissionCache
    cache = MissionCache()
    missions = cache.get_all_missions()
    return {
        "missions": missions,
        "count": len(missions)
    }
