import pytest
from backend.ai.schemas.models import IntentResponse, ClarificationResponse, Budget, Constraint, Metadata
from backend.ai.schemas.types import IntentStatus, Mission, Currency, UrgencyLevel, InventoryStatus
from backend.ai.clarification.clarification_engine import ClarificationEngine

@pytest.fixture
def base_metadata():
    return Metadata(
        timestamp="2026-07-10T12:00:00Z",
        model_version="test",
        knowledge_base_version="test",
        request_id="test",
        intent_version="v1",
        stage="intent_extraction"
    )

@pytest.fixture
def engine():
    return ClarificationEngine()

def test_high_confidence_supported(engine, base_metadata):
    intent = IntentResponse(
        intent_status=IntentStatus.SUPPORTED,
        primary_mission=Mission.HOSTEL_SETUP,
        overall_confidence=0.95,
        budget=Budget(amount=5000.0, currency=Currency.INR, confidence=0.9),
        constraints=Constraint(),
        request_metadata=base_metadata
    )
    # Give it all context so nothing else fails
    intent.keywords = ["cook", "apartment"]
    
    response = engine.generate_clarification(intent)
    assert response.needs_clarification is False
    assert len(response.questions) == 0

def test_missing_budget_global_rule(engine, base_metadata):
    intent = IntentResponse(
        intent_status=IntentStatus.SUPPORTED,
        primary_mission=Mission.HOSTEL_SETUP,
        overall_confidence=0.85, # Below high confidence threshold
        budget=Budget(currency=Currency.INR, confidence=0.0), # amount & maximum None
        constraints=Constraint(),
        request_metadata=base_metadata
    )
    # Give it all context
    intent.keywords = ["cook", "apartment"]
    
    response = engine.generate_clarification(intent)
    assert response.needs_clarification is True
    # Priority 1: Budget
    assert response.questions[0].id.value == "ASK_BUDGET"

def test_unsupported_intent(engine, base_metadata):
    intent = IntentResponse(
        intent_status=IntentStatus.UNSUPPORTED,
        overall_confidence=0.1,
        budget=Budget(),
        constraints=Constraint(),
        request_metadata=base_metadata
    )
    response = engine.generate_clarification(intent)
    assert response.needs_clarification is True
    assert response.questions[0].id.value == "ASK_MISSING_CATEGORY"

def test_ambiguous_intent(engine, base_metadata):
    intent = IntentResponse(
        intent_status=IntentStatus.AMBIGUOUS,
        overall_confidence=0.2,
        budget=Budget(maximum=1000), # Has budget
        constraints=Constraint(),
        request_metadata=base_metadata
    )
    response = engine.generate_clarification(intent)
    assert response.needs_clarification is True
    assert response.questions[0].id.value == "ASK_USAGE_CONTEXT"

def test_hostel_mission_rules_with_dependency(engine, base_metadata):
    # Hostel setup, missing budget, missing cooking, missing room type
    intent = IntentResponse(
        intent_status=IntentStatus.SUPPORTED,
        primary_mission=Mission.HOSTEL_SETUP,
        overall_confidence=0.85, # Below 0.90
        budget=Budget(), # Missing budget
        constraints=Constraint(),
        request_metadata=base_metadata
    )
    
    response = engine.generate_clarification(intent)
    assert response.needs_clarification is True
    question_ids = [q.id.value for q in response.questions]
    
    # Dependencies: ASK_ROOM_TYPE depends on ASK_COOKING.
    # Therefore, we should see ASK_BUDGET and ASK_COOKING, but NOT ASK_ROOM_TYPE.
    assert "ASK_BUDGET" in question_ids
    assert "ASK_COOKING" in question_ids
    assert "ASK_ROOM_TYPE" not in question_ids
    
    # Limit max 3 test: Should not exceed 3 questions
    assert len(response.questions) <= 3

def test_gym_goal_mission_rule(engine, base_metadata):
    intent = IntentResponse(
        intent_status=IntentStatus.SUPPORTED,
        primary_mission=Mission.GYM,
        overall_confidence=0.85,
        budget=Budget(amount=2000), # Has budget
        constraints=Constraint(),
        request_metadata=base_metadata
    )
    response = engine.generate_clarification(intent)
    assert response.needs_clarification is True
    assert response.questions[0].id.value == "ASK_GYM_GOAL"
