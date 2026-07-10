import os
import json
import time
from backend.ai.mission.exceptions import CacheLoadError
from backend.ai.mission.mission_validator import validate_aikb

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge", "current")

class MissionCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MissionCache, cls).__new__(cls)
            cls._instance._loaded = False
            cls._instance._missions = {}
            cls._instance._metadata = {}
            cls._instance._categories = []
            cls._instance._bundles = []
        return cls._instance

    def _load_json(self, filename: str):
        path = os.path.join(KNOWLEDGE_DIR, filename)
        if not os.path.exists(path):
            raise CacheLoadError(f"Missing AIKB file: {filename}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise CacheLoadError(f"Invalid JSON in {filename}: {str(e)}")

    def reload(self):
        start_time = time.time()
        
        mission_knowledge = self._load_json("mission_knowledge.json")
        bundle_knowledge = self._load_json("bundle_knowledge.json")
        supported_categories = self._load_json("supported_categories.json")
        metadata = self._load_json("metadata.json")

        validate_aikb(mission_knowledge, supported_categories, bundle_knowledge)

        # Freeze/Store
        self._categories = supported_categories
        self._bundles = bundle_knowledge
        self._metadata = metadata
        
        missions_list = mission_knowledge if isinstance(mission_knowledge, list) else mission_knowledge.get("missions", [])
        
        self._missions = {}
        for m in missions_list:
            name = m.get("mission_name", "Unknown")
            self._missions[name] = m
            
        self._loaded_at = time.time()
        self._load_time_ms = (self._loaded_at - start_time) * 1000
        self._loaded = True

    def invalidate(self):
        self._loaded = False
        self._missions = {}
        self._metadata = {}
        self._categories = []
        self._bundles = []

    def get_all_missions(self):
        if not self._loaded:
            self.reload()
        return list(self._missions.keys())

    def get_mission(self, name: str):
        if not self._loaded:
            self.reload()
        return self._missions.get(name)

    def get_metadata(self):
        if not self._loaded:
            self.reload()
        return self._metadata

    def get_load_time_ms(self):
        return getattr(self, "_load_time_ms", 0.0)

    def get_supported_categories(self):
        if not self._loaded:
            self.reload()
        return self._categories

    def get_bundle_knowledge(self):
        if not self._loaded:
            self.reload()
        return self._bundles
