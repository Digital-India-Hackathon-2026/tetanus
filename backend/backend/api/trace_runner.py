import asyncio
from httpx import AsyncClient, ASGITransport
import os
import json
from unittest.mock import patch, AsyncMock

from backend.api.main import app
from backend.ai.schemas.types import Mission, IntentStatus, Currency, InventoryStatus, UrgencyLevel
from backend.ai.schemas.models import IntentResponse, Budget, Constraint, Metadata
from backend.ai.agents.intent_agent import IntentAgent
from backend.ai.recommendation.recommendation_service import RecommendationService
from backend.ai.recommendation.config import RecommendationConfig
from backend.ai.mission.mission_service import MissionService

async def trace_query(query: str, mock_mission: Mission, budget_amt: int):
    print("="*60)
    print(f"User Query: {query} (Budget: {budget_amt})")
    print("="*60)
    
    orig_generate = RecommendationService.generate_recommendations
    
    def hooked_generate(self, query=None, mission_context=None, recommendation_context=None):
        m_context = mission_context
        r_context = recommendation_context
        print(f"MissionContext: {m_context.mission} | Categories: {m_context.primary_categories} {m_context.secondary_categories}")
        
        self.graph_repo.connect()
        categories = m_context.primary_categories + m_context.secondary_categories
        candidates = self.graph_repo.get_products_by_categories(categories, limit=self.config.max_candidates)
        print(f"Retrieval: Retrieved {len(candidates)} products from Neo4j")
        
        filtered, filter_rep = self.filter_layer.run(candidates, m_context, r_context)
        print(f"Filtering: {len(filtered)} survived. ({len(candidates)-len(filtered)} filtered)")
        
        ranked, rank_rep = self.ranking_engine.rank(filtered, m_context, r_context)
        print(f"Ranking: {len(ranked)} ranked.")
            
        div, div_rep = self.diversity_engine.enforce(ranked, m_context, r_context)
        print(f"Diversity: {len(div)} products kept.")
        
        bundles = self.bundle_builder.build_bundles(div, m_context, r_context)
        print(f"Bundles generated: {len(bundles)}")
        if bundles:
            print(f"First bundle cost: {bundles[0].total_price}")
        
        return orig_generate(self, query=query, mission_context=mission_context, recommendation_context=recommendation_context)
        
    mock_response = IntentResponse(
        intent_status=IntentStatus.SUPPORTED,
        primary_mission=mock_mission,
        secondary_missions=[],
        overall_confidence=0.9,
        categories=[],
        keywords=[query],
        budget=Budget(amount=budget_amt, maximum=budget_amt, currency=Currency.INR),
        constraints=Constraint(
            preferred_brands=[],
            excluded_brands=[],
            urgency=UrgencyLevel.NORMAL,
            preferred_price_range="mid",
            inventory_required=InventoryStatus.IN_STOCK
        ),
        request_metadata=Metadata(timestamp="2026-07-10T12:00:00Z", model_version="1", knowledge_base_version="1", request_id="123")
    )
    
    transport = ASGITransport(app=app)
    
    with patch.object(IntentAgent, "extract_intent", new_callable=AsyncMock) as mock_extract:
        with patch.object(RecommendationService, "generate_recommendations", new=hooked_generate):
            mock_extract.return_value = mock_response
            
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.post("/api/v1/recommend", json={"query": query, "profile": "balanced", "budget": budget_amt})
                
                if response.status_code != 200:
                    print(f"FAILED: {response.status_code} {response.text}")
                    return
                    
                data = response.json()
                products = data.get("products", [])
                bundles = data.get("bundles", [])
                print(f"Final API Response: {len(products)} products, {len(bundles)} bundles")
                for p in products[:3]:
                    if "product" in p:
                        print(f" - {p['product']['name']} ({p['product']['final_score']:.2f})")
                    else:
                        print(f" - Keys: {p.keys()}")

async def run_traces():
    scenarios = [
        ("I'm moving into a hostel with a budget of 5000", Mission.HOSTEL_SETUP, 5000),
        ("I need products for a birthday party", Mission.BIRTHDAY, 5000),
        ("Work from home essentials", Mission.WORK_FROM_HOME, 10000),
        ("Travel essentials", Mission.TRAVEL_ESSENTIALS, 5000),
        ("Gym setup", Mission.GYM, 5000),
        ("Movie night", Mission.MOVIE_NIGHT, 2000),
    ]
    for q, m, b in scenarios:
        await trace_query(q, m, b)

if __name__ == "__main__":
    asyncio.run(run_traces())
