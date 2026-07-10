import json
import os
from typing import Set
from backend.ai.schemas.models import IntentResponse

# Load rules configuration
RULES_PATH = os.path.join(os.path.dirname(__file__), "clarification_rules.json")
with open(RULES_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

def needs_ask_budget(intent: IntentResponse) -> bool:
    """Returns True if budget is missing."""
    return intent.budget.amount is None and intent.budget.maximum is None

def needs_ask_missing_category(intent: IntentResponse) -> bool:
    """Returns True if the intent is entirely unsupported."""
    return intent.intent_status.value == "UNSUPPORTED"

def needs_ask_usage_context(intent: IntentResponse) -> bool:
    """Returns True if intent is ambiguous."""
    return intent.intent_status.value == "AMBIGUOUS"

def needs_ask_cooking(intent: IntentResponse) -> bool:
    """Check if cooking preference is missing from Hostel Setup."""
    # If any keyword or constraint mentions cooking/food, we assume it's provided.
    text_data = " ".join(intent.keywords + intent.constraints.must_have).lower()
    return not any(w in text_data for w in ["cook", "food", "kitchen", "kettle", "stove", "induction"])

def needs_ask_room_type(intent: IntentResponse) -> bool:
    """Check if room type is missing from Hostel Setup."""
    text_data = " ".join(intent.keywords + intent.constraints.must_have).lower()
    return not any(w in text_data for w in ["single", "shared", "pg", "apartment", "flat"])

def needs_ask_gym_goal(intent: IntentResponse) -> bool:
    """Check if gym goal is missing."""
    text_data = " ".join(intent.keywords + intent.constraints.must_have).lower()
    return not any(w in text_data for w in ["weight", "muscle", "yoga", "cardio", "bulk", "cut"])

def needs_ask_trip_duration(intent: IntentResponse) -> bool:
    """Check if trip duration is missing."""
    text_data = " ".join(intent.keywords + intent.constraints.must_have).lower()
    return not any(w in text_data for w in ["weekend", "short", "long", "days", "week", "month"])

def needs_ask_work_mode(intent: IntentResponse) -> bool:
    """Check if work mode is missing."""
    text_data = " ".join(intent.keywords + intent.constraints.must_have).lower()
    return not any(w in text_data for w in ["laptop", "monitor", "desktop", "screen"])

def needs_ask_brand_preference(intent: IntentResponse) -> bool:
    """Check if brand is explicitly requested but unclear.
    If preferred_brands is empty but keywords mention a brand vaguely, ask.
    For MVP, we just check if it's missing entirely but they asked for premium."""
    return not intent.constraints.preferred_brands and intent.constraints.preferred_price_range == "premium"

# Map Question IDs to their evaluation functions
RULE_EVALUATORS = {
    "ASK_BUDGET": needs_ask_budget,
    "ASK_MISSING_CATEGORY": needs_ask_missing_category,
    "ASK_USAGE_CONTEXT": needs_ask_usage_context,
    "ASK_COOKING": needs_ask_cooking,
    "ASK_ROOM_TYPE": needs_ask_room_type,
    "ASK_GYM_GOAL": needs_ask_gym_goal,
    "ASK_TRIP_DURATION": needs_ask_trip_duration,
    "ASK_WORK_MODE": needs_ask_work_mode,
    "ASK_BRAND_PREFERENCE": needs_ask_brand_preference
}

def evaluate_rules(intent: IntentResponse) -> Set[str]:
    """Evaluates all rules and returns a set of required Question IDs."""
    required_questions = set()
    
    # 1. High Confidence Gate
    if intent.intent_status.value == "SUPPORTED" and intent.overall_confidence >= CONFIG["confidence_threshold"]:
        return required_questions
        
    # 2. Status-based gates (UNSUPPORTED/AMBIGUOUS)
    if intent.intent_status.value == "UNSUPPORTED":
        required_questions.add("ASK_MISSING_CATEGORY")
        return required_questions # Don't ask budget if we don't even know what they want
        
    if intent.intent_status.value == "AMBIGUOUS":
        required_questions.add("ASK_USAGE_CONTEXT")
        if needs_ask_budget(intent):
            required_questions.add("ASK_BUDGET")
        return required_questions
        
    # 3. Global Rules
    if needs_ask_budget(intent):
        required_questions.add("ASK_BUDGET")
        
    if needs_ask_brand_preference(intent):
        required_questions.add("ASK_BRAND_PREFERENCE")
        
    # 4. Mission-Specific Rules
    mission_name = intent.primary_mission if hasattr(intent, 'primary_mission') else None
    if mission_name and mission_name in CONFIG["mission_rules"]:
        possible_questions = CONFIG["mission_rules"][mission_name]
        for qid in possible_questions:
            if qid in RULE_EVALUATORS and RULE_EVALUATORS[qid](intent):
                required_questions.add(qid)
                
    return required_questions
