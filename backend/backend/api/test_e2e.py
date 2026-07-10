import pytest
import httpx
from httpx import ASGITransport
from backend.api.main import app
from backend.ai.schemas.models import IntentResponse, Budget, Constraint, Metadata
from backend.ai.schemas.types import IntentStatus, Currency, InventoryStatus, UrgencyLevel, Mission
from unittest.mock import patch, AsyncMock
from backend.ai.agents.intent_agent import IntentAgent

pytestmark = pytest.mark.anyio

@pytest.fixture(autouse=True)
def mock_intent_agent():
    mock_response = IntentResponse(
        intent_status=IntentStatus.SUPPORTED,
        primary_mission=Mission.WORK_FROM_HOME,
        secondary_missions=[],
        overall_confidence=0.9,
        categories=[],
        keywords=[],
        budget=Budget(amount=10000, maximum=10000, currency=Currency.INR),
        constraints=Constraint(
            preferred_brands=[],
            excluded_brands=[],
            urgency=UrgencyLevel.NORMAL,
            preferred_price_range="cheap",
            inventory_required=InventoryStatus.IN_STOCK
        ),
        request_metadata=Metadata(timestamp="2026-07-10T12:00:00Z", model_version="1", knowledge_base_version="1", request_id="123")
    )
    with patch.object(IntentAgent, "extract_intent", new_callable=AsyncMock) as mock_extract:
        mock_extract.return_value = mock_response
        yield mock_extract

async def test_clarify():
    # Test clarification endpoint
    payload = {
        "query": "I want a smartphone"
    }
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/clarify", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "needs_clarification" in data
    
async def test_recommend():
    # Test end-to-end recommendation pipeline
    payload = {
        "query": "I want a cheap smartphone under Rs 10000",
        "profile": "budget_first"
    }
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/recommend", json=payload)
        
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "mission" in data
    assert "products" in data
    assert "bundles" in data
    assert "explanation" in data
    assert "pipeline_stats" in data
