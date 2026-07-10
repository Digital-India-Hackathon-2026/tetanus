import asyncio
import os
import json
from httpx import AsyncClient, ASGITransport
from backend.api.main import app
from unittest.mock import patch
from backend.ai.schemas import IntentResponse, ExplanationResponse, Metadata, Budget, Constraint
from backend.ai.schemas.types import IntentStatus, Mission, Category
async def test_recommend_api():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        print("Testing /api/v1/health...")
        response = await ac.get("/health")
        print("Health Check:", response.json())
        print("-" * 50)
        
        print("Testing /api/v1/missions...")
        response = await ac.get("/api/v1/missions")
        print("Missions:", response.json())
        print("-" * 50)
        
        print("Testing /api/v1/recommend...")
        payload = {
            "query": "I need to set up my hostel room with a bedsheet and study lamp",
            "profile": "balanced"
        }
        
        # We need NEO4J and GEMINI_API_KEY environment variables to be set.
        # Mock Gemini responses to bypass rate limits
        mock_intent = IntentResponse(
            intent_status=IntentStatus.SUPPORTED,
            primary_mission=Mission.HOSTEL_SETUP,
            secondary_missions=[],
            categories=[Category.HOME, Category.ELECTRONICS],
            budget=Budget(),
            constraints=Constraint(),
            overall_confidence=0.95,
            needs_clarification=False,
            questions=[],
            request_metadata=Metadata(
                timestamp="2026-07-10T15:51:54Z",
                model_version="gemini-2.5-flash",
                knowledge_base_version="current",
                request_id="test-req-id"
            )
        )
        mock_expl = ExplanationResponse(
            mission=Mission.HOSTEL_SETUP,
            recommended_products=["Product 1", "Product 2"],
            recommendation_reasons={"Product 1": "Reason 1", "Product 2": "Reason 2"},
            bundles=[],
            budget_summary="Within budget.",
            inventory_summary="All in stock.",
            alternative_products=[]
        )
        
        with patch("backend.ai.agents.intent_agent.IntentAgent.extract_intent", return_value=mock_intent), \
             patch("backend.ai.agents.explanation_agent.ExplanationAgent.generate_explanation", return_value=mock_expl):
            response = await ac.post("/api/v1/recommend", json=payload, timeout=60.0)
        
        if response.status_code == 200:
            print("Response Data:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error {response.status_code}:", response.text)

if __name__ == "__main__":
    asyncio.run(test_recommend_api())
