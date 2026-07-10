import hashlib
import json
import time
import logging
from backend.ai.mission.mission_models import MissionContext, MissionMetadata
from backend.ai.mission.mission_loader import MissionLoader
from backend.ai.mission.exceptions import MissionNotFoundError
from backend.ai.mission.mission_config import UNSUPPORTED_KEYWORDS, normalize_categories

logger = logging.getLogger(__name__)

class MissionService:
    def __init__(self):
        self.loader = MissionLoader()

    def _is_unsupported(self, query: str) -> bool:
        """Checks if a query contains any unsupported keywords."""
        if not query:
            return False
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in UNSUPPORTED_KEYWORDS)

    def resolve(self, intent_response: dict, raw_query: str = "") -> MissionContext:
        start_time = time.time()
        
        mission_name = intent_response.get("primary_mission")
        if not mission_name:
            raise MissionNotFoundError("No mission provided in IntentResponse.")
            
        # Check for unsupported missions early
        if self._is_unsupported(raw_query) or self._is_unsupported(mission_name):
            logger.info(f"Unsupported mission detected: {mission_name} / {raw_query}")
            return MissionContext(
                mission=mission_name,
                supported=False,
                definition={},
                primary_categories=[],
                secondary_categories=[],
                required_categories=[],
                optional_categories=[],
                category_weights={},
                bundle_ids=[],
                priority="LOW",
                mission_type="unsupported",
                metadata=MissionMetadata(
                    aikb_version="unknown", schema_version="v1", generated_at="unknown",
                    mission_hash="unsupported", source="UNSUPPORTED", loaded_from="N/A", load_time_ms=0.0
                )
            )

        m_data = self.loader.load_mission(mission_name)
        if not m_data:
            raise MissionNotFoundError(f"Mission '{mission_name}' is not supported by the AIKB.")

        # Hash Generation (deterministic from definition)
        m_string = json.dumps(m_data, sort_keys=True)
        m_hash = hashlib.sha256(m_string.encode('utf-8')).hexdigest()

        kb_meta = self.loader.get_metadata()
        
        # Build Metadata
        meta = MissionMetadata(
            aikb_version=kb_meta.get("knowledge_base_version", "unknown"),
            schema_version="v1",
            generated_at=kb_meta.get("generation_timestamp", "unknown"),
            mission_hash=m_hash,
            source="AIKB",
            loaded_from="mission_knowledge.json",
            load_time_ms=self.loader.get_load_time_ms()
        )

        # Extract Fields and Normalize Categories
        req_cats = normalize_categories(m_data.get("required_categories", []))
        opt_cats = normalize_categories(m_data.get("optional_categories", []))
        prim_cats = normalize_categories(m_data.get("primary_categories", []))
        sec_cats = normalize_categories(m_data.get("secondary_categories", []))
        weights = m_data.get("category_weights", {})
        priority = m_data.get("priority", "NORMAL")
        m_type = m_data.get("mission_type", "UNKNOWN")
        
        # Bundles
        bundles_list = m_data.get("bundles", [])
        b_ids = [b.get("bundle_name", b.get("name", "")) if isinstance(b, dict) else b for b in bundles_list]

        # Construct MissionContext
        context = MissionContext(
            mission=mission_name,
            supported=True,
            definition=m_data,
            primary_categories=prim_cats,
            secondary_categories=sec_cats,
            required_categories=req_cats,
            optional_categories=opt_cats,
            category_weights=weights,
            bundle_ids=b_ids,
            priority=priority,
            mission_type=m_type,
            metadata=meta
        )

        exec_time = (time.time() - start_time) * 1000
        logger.info(f"Resolved Mission: {mission_name} | Type: {m_type} | Priority: {priority} | Categories: {len(prim_cats)+len(sec_cats)} | Bundles: {len(b_ids)} | Hash: {m_hash[:8]} | Time: {exec_time:.2f}ms")

        return context
