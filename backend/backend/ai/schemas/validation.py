from typing import Any
from .models import Budget, Constraint, IntentResponse, ExplanationResponse
from pydantic import ValidationError

def validate_budget(data: dict) -> bool:
    try:
        Budget(**data)
        return True
    except ValidationError:
        return False

def validate_mission(mission_str: str) -> bool:
    from .types import Mission
    try:
        Mission(mission_str)
        return True
    except ValueError:
        return False

def validate_category(category_str: str) -> bool:
    from .types import Category
    try:
        Category(category_str)
        return True
    except ValueError:
        return False

def validate_response(data: dict) -> bool:
    try:
        IntentResponse(**data)
        return True
    except ValidationError:
        return False
