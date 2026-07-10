import os
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

from .runtime_config import RuntimeConfig
from .prompt_cache import MemoryCache
from .exceptions import MissingDependencyError, ManifestValidationError

class ContextBuilder:
    """Responsible for loading AIKB and Schema files from disk via cache."""
    
    def __init__(self, cache: MemoryCache):
        self.cache = cache
        
    def _read_json_file(self, filepath: Path) -> Any:
        if not filepath.exists():
            raise MissingDependencyError(f"Required dependency not found: {filepath}")
            
        mtime = os.path.getmtime(filepath)
        cache_key = str(filepath)
        
        cached_value, hit = self.cache.get(cache_key, check_mtime=mtime)
        if hit:
            return cached_value, True
            
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.cache.set(cache_key, data, mtime=mtime)
        return data, False
        
    def build_aikb_context(self, dependencies: List[str]) -> Tuple[Dict[str, Any], Dict[str, int]]:
        """Loads specific AIKB JSON files. Returns (context_dict, metrics)."""
        aikb = {}
        hits = 0
        misses = 0
        
        for filename in dependencies:
            filepath = RuntimeConfig.KNOWLEDGE_DIR / filename
            data, hit = self._read_json_file(filepath)
            
            # Use filename without extension as key (e.g., 'mission_catalog')
            key = Path(filename).stem
            aikb[key] = data
            
            if hit: hits += 1
            else: misses += 1
            
        return aikb, {"hits": hits, "misses": misses}
        
    def build_schema_context(self, dependencies: List[str]) -> Tuple[Dict[str, Any], Dict[str, int]]:
        """Loads specific Schema JSON files."""
        schemas = {}
        hits = 0
        misses = 0
        
        for filename in dependencies:
            filepath = RuntimeConfig.SCHEMAS_DIR / filename
            data, hit = self._read_json_file(filepath)
            
            key = Path(filename).stem
            schemas[key] = data
            
            if hit: hits += 1
            else: misses += 1
            
        return schemas, {"hits": hits, "misses": misses}

    def load_prompt_manifest(self) -> Dict[str, Any]:
        filepath = RuntimeConfig.PROMPTS_DIR / "prompt_manifest.json"
        if not filepath.exists():
            raise ManifestValidationError("prompt_manifest.json is missing.")
        data, _ = self._read_json_file(filepath)
        return data
