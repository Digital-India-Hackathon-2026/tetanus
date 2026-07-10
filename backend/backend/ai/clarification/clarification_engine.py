import json
import os
from typing import List

from backend.ai.schemas.models import IntentResponse, ClarificationResponse, ClarificationQuestion
from backend.ai.schemas.types import QuestionID, QuestionType
from backend.ai.clarification.rules import evaluate_rules, CONFIG

CATALOG_PATH = os.path.join(os.path.dirname(__file__), "question_catalog.json")
with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    CATALOG = json.load(f)

class ClarificationEngine:
    def __init__(self):
        self.catalog = CATALOG
        self.priorities = CONFIG.get("priorities", [])
        self.dependencies = CONFIG.get("dependencies", {})
        self.max_questions = CONFIG.get("max_questions", 3)

    def generate_clarification(self, intent: IntentResponse) -> ClarificationResponse:
        """Determines if clarification is needed and returns the questions."""
        required_ids = evaluate_rules(intent)
        
        # Apply Skip Logic / Dependencies
        # E.g., if ASK_ROOM_TYPE depends on ASK_COOKING, and ASK_COOKING is in the required set,
        # we do not ask ASK_ROOM_TYPE yet.
        filtered_ids = set()
        for qid in required_ids:
            deps = self.dependencies.get(qid, [])
            if any(dep in required_ids for dep in deps):
                # Skip this question for now because a dependency is also being asked
                continue
            filtered_ids.add(qid)
            
        # Priority Ordering
        ordered_ids = []
        for qid in self.priorities:
            if qid in filtered_ids:
                ordered_ids.append(qid)
                
        # Append any unprioritized questions at the end
        for qid in filtered_ids:
            if qid not in ordered_ids:
                ordered_ids.append(qid)
                
        # Limit to max questions
        final_ids = ordered_ids[:self.max_questions]
        
        if not final_ids:
            return ClarificationResponse(
                needs_clarification=False,
                questions=[],
                reason="No clarification required based on deterministic rules."
            )
            
        # Build ClarificationQuestion objects
        questions = []
        for qid in final_ids:
            q_data = self.catalog.get(qid)
            if not q_data:
                continue
            
            questions.append(
                ClarificationQuestion(
                    id=QuestionID(qid),
                    question=q_data["question"],
                    type=QuestionType(q_data["type"]),
                    options=q_data.get("options", [])
                )
            )
            
        reason = f"Missing required context. Top priority: {final_ids[0]}"
        if "ASK_MISSING_CATEGORY" in final_ids:
            reason = "Unsupported intent requires category selection."
        elif "ASK_USAGE_CONTEXT" in final_ids:
            reason = "Ambiguous intent requires context clarification."
            
        return ClarificationResponse(
            needs_clarification=True,
            questions=questions,
            reason=reason
        )
