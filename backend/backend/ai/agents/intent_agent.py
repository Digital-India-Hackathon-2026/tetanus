import os
import re
import json
import time
import uuid
import logging
import unicodedata
from datetime import datetime
from typing import Optional, Dict, Any, List

from backend.ai.gemini import GeminiClient, GeminiModel
from backend.ai.runtime import PromptRenderer, PromptContext
from backend.ai.schemas import IntentResponse, ClarificationQuestion, Metadata, QuestionType
from backend.ai.gemini.exceptions import GeminiAPIError

logger = logging.getLogger("CIN.IntentAgent")

class IntentAgent:
    """
    The Intent Extraction Agent responsible for parsing user queries into a
    structured IntentResponse contract using the Gemini client and Prompt renderer.
    """
    
    def __init__(self, gemini_client: Optional[GeminiClient] = None):
        self.gemini_client = gemini_client or GeminiClient()
        self.renderer = PromptRenderer()
        self.log_dir = "backend/ai/logs/invalid_intent_responses"
        os.makedirs(self.log_dir, exist_ok=True)

    def _repair_json(self, raw_text: str) -> str:
        """
        Lightweight JSON repair pipeline:
        - Removes markdown code fences
        - Strips whitespace
        - Fixes trailing commas inside arrays/objects
        """
        cleaned = raw_text.strip()
        
        # Remove markdown fences
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.strip()
        
        # Remove trailing commas before closing braces/brackets
        cleaned = re.sub(r",\s*([\]}])", r"\1", cleaned)
        
        return cleaned

    def _normalize_input(self, raw_input: str) -> str:
        """Cleans user input before passing to Gemini."""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', raw_input).strip()
        # Remove control characters
        cleaned = "".join(ch for ch in cleaned if unicodedata.category(ch)[0] != "C")
        return cleaned

    def _normalize_output(self, data: dict) -> None:
        """Normalizes output fields against AIKB."""
        kb_path = "backend/ai/knowledge/current"
        try:
            with open(f"{kb_path}/mission_catalog.json", "r", encoding="utf-8") as f:
                missions = [m["mission_name"] for m in json.load(f)]
        except:
            missions = []
            
        try:
            with open(f"{kb_path}/supported_categories.json", "r", encoding="utf-8") as f:
                categories = [c.get("category_name") for c in json.load(f)]
        except:
            categories = []

        pm = data.get("primary_mission")
        if pm:
            for m in missions:
                if pm.strip().lower() == m.lower():
                    data["primary_mission"] = m
                    break

        new_sm = []
        for s in data.get("secondary_missions", []):
            matched = False
            for m in missions:
                if s.strip().lower() == m.lower():
                    new_sm.append(m)
                    matched = True
                    break
            if not matched:
                new_sm.append(s)
        data["secondary_missions"] = new_sm

        new_cats = []
        for c in data.get("categories", []):
            matched = False
            for ac in categories:
                if c.strip().lower() == ac.lower():
                    new_cats.append(ac)
                    matched = True
                    break
            if not matched:
                new_cats.append(c)
        data["categories"] = new_cats

    def _save_invalid_response(self, query: str, raw_response: str, error_msg: str) -> None:
        """Dumps invalid responses to logs folder for debugging."""
        filename = f"failed_{int(time.time())}_{uuid.uuid4().hex[:6]}.json"
        filepath = os.path.join(self.log_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({
                    "timestamp": datetime.utcnow().isoformat(),
                    "query": query,
                    "raw_response": raw_response,
                    "error": error_msg
                }, f, indent=2)
            logger.warning(f"Saved invalid response telemetry to: {filepath}")
        except Exception as e:
            logger.error(f"Failed to save invalid response: {e}")

    def _apply_confidence_rules(self, data: dict) -> None:
        """Enforces confidence thresholds programmatically in Python."""
        confidence = data.get("overall_confidence", 0.0)
        
        if confidence >= 0.90:
            data["needs_clarification"] = False
            data["questions"] = []
        elif 0.70 <= confidence < 0.90:
            # Clarification only if essential fields (like budget min/max) are completely missing
            budget = data.get("budget", {})
            has_budget = budget.get("amount") is not None or budget.get("maximum") is not None
            if has_budget:
                data["needs_clarification"] = False
                data["questions"] = []
            else:
                data["needs_clarification"] = True
        else:
            # confidence < 0.70
            data["needs_clarification"] = True
            if not data.get("questions"):
                # Inject a fallback question if LLM forgot to provide one
                data["questions"] = [{
                    "id": "ASK_USAGE_CONTEXT",
                    "question": "Could you please specify what shopping mission or items you need?",
                    "type": "SINGLE_SELECT",
                    "options": ["Hostel Setup", "Gym Starter", "Weekly Grocery", "Office Setup", "Snacks"]
                }]

        # Ensure max 3 questions
        if "questions" in data and len(data["questions"]) > 3:
            data["questions"] = data["questions"][:3]

    async def extract_intent(self, user_query: str, session_id: Optional[str] = None, request_id: Optional[str] = None) -> IntentResponse:
        """
        Extracts user intent from natural language asynchronously.
        """
        req_id = request_id or str(uuid.uuid4())
        
        normalized_query = self._normalize_input(user_query)
        
        # 1. Initialize Context
        context = PromptContext(
            user_input=normalized_query,
            knowledge_version="current",
            prompt_version="v1",
            schema_version="v1",
            request_id=req_id,
            session_id=session_id
        )

        # 2. Render Examples & Rules Prompts
        rules_request = self.renderer.render("intent_rules", "v1", context)
        context.variables["rules"] = rules_request.rendered_text

        examples_request = self.renderer.render("intent_examples", "v1", context)
        context.variables["few_shot_examples"] = examples_request.rendered_text

        # 3. Render System Prompt
        system_request = self.renderer.render("intent_system", "v1", context)

        # 4. Trigger Gemini Call
        try:
            gemini_response = await self.gemini_client.generate_content(
                prompt=system_request.rendered_text,
                model=GeminiModel.GEMINI_FLASH_LITE_LATEST,
                temperature=0.0
            )
            raw_text = gemini_response.text
        except Exception as e:
            logger.error(f"Gemini API failure during intent extraction: {e}")
            raise GeminiAPIError(f"API call failed: {e}")

        prompt_tokens = gemini_response.usage.prompt_tokens if gemini_response.usage else 0
        output_tokens = gemini_response.usage.response_tokens if gemini_response.usage else 0
        latency_ms = gemini_response.latency

        # 5. Repair JSON
        repaired_text = self._repair_json(raw_text)

        # 6. Parse JSON dict
        try:
            parsed_data = json.loads(repaired_text)
        except Exception as e:
            self._save_invalid_response(user_query, raw_text, f"JSON parsing failed: {e}")
            raise GeminiAPIError(f"Response was not valid JSON: {e}")

        # 7. Apply Output Normalization & Confidence Logic
        self._normalize_output(parsed_data)
        self._apply_confidence_rules(parsed_data)

        # 8. Inject request metadata programmatically
        metadata_dict = {
            "language": context.language,
            "country": context.country,
            "currency": "INR",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model_version": GeminiModel.GEMINI_FLASH_LITE_LATEST.value,
            "knowledge_base_version": "current",
            "request_id": req_id,
            "session_id": session_id,
            "intent_version": "v1",
            "stage": "intent_extraction",
            "prompt_tokens": prompt_tokens,
            "output_tokens": output_tokens,
            "latency_ms": latency_ms
        }
        parsed_data["request_metadata"] = metadata_dict

        # 9. Pydantic validation
        try:
            validated_response = IntentResponse(**parsed_data)
            return validated_response
        except Exception as e:
            self._save_invalid_response(user_query, raw_text, f"Pydantic validation failed: {e}")
            raise GeminiAPIError(f"Response did not match target schemas: {e}")
