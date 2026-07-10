import asyncio
from httpx import AsyncClient, ASGITransport
from backend.api.main import app
from backend.ai.schemas.types import Mission
from unittest.mock import patch, AsyncMock
from backend.ai.agents.intent_agent import IntentAgent
from backend.ai.schemas.models import IntentResponse, Budget, Constraint, Metadata
from backend.ai.schemas.types import IntentStatus, Currency, InventoryStatus, UrgencyLevel

async def run_audit():
    scenarios = [
        ("I'm moving into a hostel.", Mission.HOSTEL_SETUP),
        ("I need a birthday party.", Mission.BIRTHDAY),
        ("Gym under Rs 3000", Mission.GYM),
        ("Kitchen setup", Mission.WORK_FROM_HOME), # Using fallback
        ("Travel essentials", Mission.TRAVEL_ESSENTIALS),
        ("Movie night", Mission.MOVIE_NIGHT),
        ("Work from home", Mission.WORK_FROM_HOME)
    ]

    transport = ASGITransport(app=app)
    
    # We MUST mock IntentAgent because Gemini Free Tier only allows 20 req/day.
    # We will verify the rest of the pipeline end-to-end.
    for query, mission in scenarios:
        print(f"Testing scenario: '{query}' with mocked mission {mission.value}")
        
        mock_response = IntentResponse(
            intent_status=IntentStatus.SUPPORTED,
            primary_mission=mission,
            secondary_missions=[],
            overall_confidence=0.9,
            categories=[],
            keywords=["test"],
            budget=Budget(amount=5000, maximum=5000, currency=Currency.INR),
            constraints=Constraint(
                preferred_brands=[],
                excluded_brands=[],
                urgency=UrgencyLevel.NORMAL,
                preferred_price_range="mid",
                inventory_required=InventoryStatus.IN_STOCK
            ),
            request_metadata=Metadata(timestamp="2026-07-10T12:00:00Z", model_version="1", knowledge_base_version="1", request_id="123")
        )
        
        with patch.object(IntentAgent, "extract_intent", new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = mock_response
            
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.post("/api/v1/recommend", json={"query": query, "profile": "balanced"})
                if response.status_code == 200:
                    data = response.json()
                    products = data.get("recommended_products", [])
                    bundles = data.get("bundles", [])
                    print(f"  -> SUCCESS! Found {len(products)} products, {len(bundles)} bundles")
                else:
                    print(f"  -> FAILED! {response.status_code} {response.text}")

if __name__ == "__main__":
    asyncio.run(run_audit())
