import pytest
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
