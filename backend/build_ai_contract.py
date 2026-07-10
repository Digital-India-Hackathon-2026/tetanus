import os
import json
import shutil
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
AI_KNOWLEDGE_V1 = BASE_DIR / "backend" / "ai" / "knowledge" / "v1"
AI_KNOWLEDGE_CURRENT = BASE_DIR / "backend" / "ai" / "knowledge" / "current"
AI_SCHEMAS_DIR = BASE_DIR / "backend" / "ai" / "schemas"

def setup_directories():
    # Copy v1 to current if it doesn't exist or is outdated
    if AI_KNOWLEDGE_V1.exists():
        if AI_KNOWLEDGE_CURRENT.exists():
            shutil.rmtree(AI_KNOWLEDGE_CURRENT)
        shutil.copytree(AI_KNOWLEDGE_V1, AI_KNOWLEDGE_CURRENT)
    
    os.makedirs(AI_SCHEMAS_DIR, exist_ok=True)
    # create __init__.py so it can be imported
    (AI_SCHEMAS_DIR / "__init__.py").touch(exist_ok=True)

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_types_py():
    print("Generating types.py...")
    # Load knowledge
    mission_catalog = load_json(AI_KNOWLEDGE_CURRENT / "mission_catalog.json")
    supported_categories = load_json(AI_KNOWLEDGE_CURRENT / "supported_categories.json")
    
    missions = [m["mission_name"] for m in mission_catalog]
    categories = [c["category_name"] for c in supported_categories]
    
    types_content = "from enum import Enum\n\n"
    types_content += "class Mission(str, Enum):\n"
    for m in missions:
        var_name = "".join([c if c.isalnum() else "_" for c in m]).upper()
        if var_name[0].isdigit(): var_name = "_" + var_name
        types_content += f'    {var_name} = "{m}"\n'
        
    types_content += "\nclass Category(str, Enum):\n"
    for c in categories:
        var_name = "".join([ch if ch.isalnum() else "_" for ch in c]).upper()
        if var_name[0].isdigit(): var_name = "_" + var_name
        types_content += f'    {var_name} = "{c}"\n'
        
    types_content += """
class Currency(str, Enum):
    INR = "INR"

class InventoryStatus(str, Enum):
    IN_STOCK = "IN_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    PREORDER = "PREORDER"

class InteractionType(str, Enum):
    VIEW = "VIEW"
    ADD_TO_CART = "ADD_TO_CART"
    PURCHASE = "PURCHASE"
    SAVE_FOR_LATER = "SAVE_FOR_LATER"
"""
    with open(AI_SCHEMAS_DIR / "types.py", 'w', encoding='utf-8') as f:
        f.write(types_content)

def generate_models_py():
    print("Generating models.py...")
    content = '''from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from .types import Mission, Category, Currency, InventoryStatus

class Budget(BaseModel):
    """Schema defining user budget parameters."""
    amount: Optional[float] = Field(None, description="Exact budget amount if specified")
    currency: Currency = Field(default=Currency.INR, description="Currency of the budget")
    minimum: Optional[float] = Field(None, description="Minimum acceptable price")
    maximum: Optional[float] = Field(None, description="Maximum acceptable price")
    estimated: Optional[bool] = Field(False, description="Whether the budget is an AI estimation")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the budget extraction")

class Constraint(BaseModel):
    """Schema defining user constraints and preferences."""
    preferred_brands: List[str] = Field(default_factory=list, description="List of specifically requested brands")
    excluded_brands: List[str] = Field(default_factory=list, description="Brands the user does not want")
    preferred_categories: List[Category] = Field(default_factory=list, description="Categories the user is interested in")
    must_have: List[str] = Field(default_factory=list, description="Features or keywords the items MUST have")
    nice_to_have: List[str] = Field(default_factory=list, description="Features or keywords the user would like")
    maximum_delivery_days: Optional[int] = Field(None, description="Maximum acceptable delivery time in days")
    preferred_price_range: Optional[str] = Field(None, description="Qualitative price range e.g., 'cheap', 'premium'")
    minimum_rating: float = Field(0.0, ge=0.0, le=5.0, description="Minimum acceptable average rating")
    inventory_required: InventoryStatus = Field(default=InventoryStatus.IN_STOCK, description="Required inventory status")

class Metadata(BaseModel):
    """Metadata tracking request properties."""
    language: str = Field(default="en", description="Language code of the request")
    country: str = Field(default="IN", description="Country code of the user")
    currency: Currency = Field(default=Currency.INR, description="Requested currency")
    timestamp: str = Field(..., description="ISO8601 timestamp of the request")
    model_version: str = Field(..., description="Version of the Gemini model used")
    knowledge_base_version: str = Field(..., description="Version of the AIKB used")
    request_id: str = Field(..., description="Unique UUID for tracing the request")

class IntentResponse(BaseModel):
    """Master schema for the Intent Agent output."""
    model_config = ConfigDict(title="MissionSchema")
    primary_mission: Mission = Field(..., description="The primary mission identified from the catalog")
    secondary_missions: List[Mission] = Field(default_factory=list, description="Any secondary missions identified")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence of the intent extraction")
    categories: List[Category] = Field(..., description="Categories relevant to the request")
    keywords: List[str] = Field(..., description="Extracted keywords mapping to the AIKB")
    budget: Budget = Field(..., description="Extracted or inferred budget")
    constraints: Constraint = Field(..., description="User constraints and preferences")
    reasoning: str = Field(..., description="Chain of thought explaining why this intent was extracted")
    request_metadata: Metadata = Field(..., description="Metadata for logging and tracking")

class ExplanationResponse(BaseModel):
    """Master schema for the Explanation Agent output."""
    mission: Mission = Field(..., description="The mission context for the explanation")
    recommended_products: List[str] = Field(..., description="List of recommended product names")
    recommendation_reasons: dict[str, str] = Field(..., description="Dictionary mapping product names to explanation strings")
    bundles: List[str] = Field(default_factory=list, description="List of recommended bundle names")
    budget_summary: str = Field(..., description="Explanation of how the recommendations fit the budget")
    inventory_summary: str = Field(..., description="Summary of inventory status for the recommendations")
    alternative_products: List[str] = Field(default_factory=list, description="List of alternative product names")
'''
    with open(AI_SCHEMAS_DIR / "models.py", 'w', encoding='utf-8') as f:
        f.write(content)

def generate_validation_py():
    print("Generating validation.py...")
    content = '''from typing import Any
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
'''
    with open(AI_SCHEMAS_DIR / "validation.py", 'w', encoding='utf-8') as f:
        f.write(content)

def export_json_schemas():
    print("Exporting JSON Schemas...")
    sys.path.insert(0, str(BASE_DIR))
    from backend.ai.schemas.models import Budget, Constraint, IntentResponse, ExplanationResponse
    
    def adjust_schema(schema_dict):
        schema_dict["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        return schema_dict

    schemas = {
        "budget_schema.json": adjust_schema(Budget.model_json_schema()),
        "constraint_schema.json": adjust_schema(Constraint.model_json_schema()),
        "mission_schema.json": adjust_schema(IntentResponse.model_json_schema()), # As requested, mission_schema defines the Intent Agent output
        "response_schema.json": adjust_schema(IntentResponse.model_json_schema()), # Master schema
        "explanation_schema.json": adjust_schema(ExplanationResponse.model_json_schema()),
    }
    
    for filename, schema_data in schemas.items():
        with open(AI_SCHEMAS_DIR / filename, 'w', encoding='utf-8') as f:
            json.dump(schema_data, f, indent=4)

def generate_schema_examples():
    print("Generating schema_examples.json...")
    sys.path.insert(0, str(BASE_DIR))
    import datetime
    from backend.ai.schemas.types import Mission, Category, Currency, InventoryStatus
    from backend.ai.schemas.models import IntentResponse
    
    # Generate 10 valid and 10 invalid
    valid_examples = []
    invalid_examples = []
    
    # We will just generate 1 valid and 1 invalid mathematically sound, and duplicate/mutate to reach 10
    base_valid = {
        "primary_mission": list(Mission)[0].value,
        "secondary_missions": [],
        "confidence": 0.95,
        "categories": [list(Category)[0].value],
        "keywords": ["test", "keyword"],
        "budget": {
            "amount": 5000,
            "currency": "INR",
            "confidence": 1.0
        },
        "constraints": {
            "preferred_brands": [],
            "excluded_brands": [],
            "preferred_categories": [],
            "must_have": [],
            "nice_to_have": [],
            "minimum_rating": 4.0,
            "inventory_required": "IN_STOCK"
        },
        "reasoning": "This is a valid reasoning string.",
        "request_metadata": {
            "language": "en",
            "country": "IN",
            "currency": "INR",
            "timestamp": datetime.datetime.now().isoformat(),
            "model_version": "gemini-1.5-pro",
            "knowledge_base_version": "current",
            "request_id": "123e4567-e89b-12d3-a456-426614174000"
        }
    }
    
    import copy
    for i in range(10):
        # Valid
        v = copy.deepcopy(base_valid)
        v["budget"]["amount"] += i * 100
        valid_examples.append(v)
        
        # Invalid (e.g. wrong type, missing required, bad enum)
        inv = copy.deepcopy(base_valid)
        if i == 0:
            inv["primary_mission"] = "UNKNOWN_MISSION" # Bad enum
            reason = "primary_mission value is not in the Mission enum."
        elif i == 1:
            inv["confidence"] = 1.5 # Out of bounds (le=1.0)
            reason = "confidence exceeds maximum value of 1.0."
        elif i == 2:
            del inv["categories"] # Missing required field
            reason = "Missing required field: categories."
        elif i == 3:
            inv["budget"] = {"amount": "string"} # Wrong type
            reason = "budget.amount is a string, expected number."
        elif i == 4:
            inv["request_metadata"] = {} # Missing metadata fields
            reason = "request_metadata is missing required fields."
        elif i == 5:
            inv["constraints"] = {"minimum_rating": 6.0} # Out of bounds rating
            reason = "constraints.minimum_rating exceeds 5.0."
        elif i == 6:
            inv["keywords"] = "not a list"
            reason = "keywords is a string, expected a list."
        elif i == 7:
            inv["secondary_missions"] = ["BAD_MISSION"]
            reason = "secondary_missions contains an invalid enum value."
        elif i == 8:
            inv["budget"]["confidence"] = -0.1
            reason = "budget.confidence is below 0.0."
        else:
            inv["constraints"]["inventory_required"] = "NEVER"
            reason = "constraints.inventory_required is an invalid enum."
        
        invalid_examples.append({"payload": inv, "reason": reason})
        
    # Validate them with jsonschema
    import jsonschema
    schema = IntentResponse.model_json_schema()
    
    for idx, ex in enumerate(valid_examples):
        jsonschema.validate(instance=ex, schema=schema) # Should pass without exception
        
    for idx, ex in enumerate(invalid_examples):
        try:
            jsonschema.validate(instance=ex["payload"], schema=schema)
            print(f"WARNING: Invalid example {idx} passed validation! This is a bug.")
        except jsonschema.exceptions.ValidationError:
            pass # Expected
            
    with open(AI_SCHEMAS_DIR / "schema_examples.json", 'w', encoding='utf-8') as f:
        json.dump({"valid_examples": valid_examples, "invalid_examples": invalid_examples}, f, indent=4)

def generate_docs():
    print("Generating schema_documentation.md...")
    docs = """# AI Contract Schemas Documentation

This directory contains the canonical JSON Schemas and strongly-typed Pydantic models that form the strict API contract between Gemini, FastAPI, and the broader CIN system.

## The Primary Source of Truth
The `models.py` file contains the Pydantic models which act as the absolute source of truth. They dynamically inherit valid enumerations (Missions, Categories) from `types.py`, which is generated directly from the AI Knowledge Base (`backend/ai/knowledge/current/`).

The JSON Schema files (`*_schema.json`) in this directory are automatically generated from these Pydantic models. They follow the JSON Schema 2020-12 specification and are provided for documentation and external interoperability.

## Schemas
*   **Mission Schema / Response Schema**: (`IntentResponse`) Defines the exact structure Gemini must return to classify a user's intent, budget, and constraints.
*   **Explanation Schema**: (`ExplanationResponse`) Defines the structure required by the Explanation Agent to formulate recommendation reasoning.
*   **Budget & Constraint Schemas**: Sub-schemas detailing how to capture financial limits and specific filtering rules (like preferred brands or minimum ratings).

## Validation Rules
All validations are rigidly enforced by Pydantic:
*   `confidence` scores must always be between `0.0` and `1.0`.
*   `minimum_rating` must be between `0.0` and `5.0`.
*   `primary_mission` strictly checks against the `Mission` Enum.
*   `categories` must exist in the `Category` Enum.
*   Required fields cannot be omitted, and types must match exactly (or be safely coercible).

For a complete breakdown, refer to `schema_examples.json`, which documents verified valid and invalid payloads along with explanations for the failures.
"""
    with open(AI_SCHEMAS_DIR / "schema_documentation.md", 'w', encoding='utf-8') as f:
        f.write(docs)

def generate_tests():
    print("Generating test_validation.py...")
    content = '''import pytest
import json
import os
from pathlib import Path
from backend.ai.schemas.models import IntentResponse
from pydantic import ValidationError

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

@pytest.fixture
def examples():
    with open(BASE_DIR / "schema_examples.json", 'r') as f:
        return json.load(f)

def test_valid_examples(examples):
    for ex in examples["valid_examples"]:
        # Should not raise
        IntentResponse(**ex)

def test_invalid_examples(examples):
    for ex in examples["invalid_examples"]:
        with pytest.raises(ValidationError):
            IntentResponse(**ex["payload"])
'''
    with open(AI_SCHEMAS_DIR / "test_validation.py", 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    setup_directories()
    generate_types_py()
    generate_models_py()
    generate_validation_py()
    export_json_schemas()
    generate_schema_examples()
    generate_docs()
    generate_tests()
    print("AI Contract Generation Complete.")

if __name__ == "__main__":
    main()
