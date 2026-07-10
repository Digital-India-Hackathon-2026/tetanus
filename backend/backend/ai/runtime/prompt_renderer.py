import time
import os
from pathlib import Path
from typing import Dict, Any
import warnings

from .runtime_config import RuntimeConfig
from .runtime_models import PromptContext, PromptRequest, RuntimeMetadata
from .template_engine import TemplateEngine
from .prompt_cache import MemoryCache
from .context_builder import ContextBuilder
from .exceptions import ManifestValidationError, PromptValidationError, OversizedPromptWarning, MissingDependencyError

class PromptRenderer:
    """
    Main orchestrator for assembling prompts.
    Loads AIKB, schemas, templates, checks cache, and renders the final PromptRequest.
    """
    
    def __init__(self):
        self.cache = MemoryCache(ttl_seconds=RuntimeConfig.CACHE_TTL_SECONDS)
        self.context_builder = ContextBuilder(self.cache)
        self.template_engine = TemplateEngine()

    def _read_template_file(self, filename: str) -> str:
        filepath = RuntimeConfig.PROMPTS_DIR / filename
        if not filepath.exists():
            raise PromptValidationError(f"Prompt template missing: {filename}")
            
        mtime = os.path.getmtime(filepath)
        cache_key = str(filepath)
        
        cached_value, hit = self.cache.get(cache_key, check_mtime=mtime)
        if hit:
            return cached_value, True
            
        with open(filepath, 'r', encoding='utf-8') as f:
            template_str = f.read()
            
        self.cache.set(cache_key, template_str, mtime=mtime)
        return template_str, False

    def render(self, prompt_name: str, version: str, context_vars: PromptContext) -> PromptRequest:
        """
        Renders a specific prompt version using the provided context.
        """
        start_time = time.time()
        
        # 1. Load Manifest
        manifest = self.context_builder.load_prompt_manifest()
        
        if prompt_name not in manifest["prompts"]:
            raise ManifestValidationError(f"Prompt '{prompt_name}' not found in manifest.")
            
        prompt_config = manifest["prompts"][prompt_name]["versions"].get(version)
        if not prompt_config:
            raise ManifestValidationError(f"Version '{version}' not found for prompt '{prompt_name}'.")

        # 2. Validate User Provided Variables
        required_vars = set(prompt_config.get("required_variables", []))
        provided_vars = set(context_vars.variables.keys())
        
        # We manually add user_input, language, etc to provided vars for validation
        core_vars = {"user_input", "language", "country", "session_id", "request_id"}
        provided_vars.update(core_vars)
        
        missing = required_vars - provided_vars
        if missing:
            raise PromptValidationError(f"Missing required variables for {prompt_name} {version}: {missing}")

        # 3. Load Dependencies via Context Builder
        aikb_deps = prompt_config.get("aikb_dependencies", [])
        schema_deps = prompt_config.get("schema_dependencies", [])
        
        aikb_data, aikb_metrics = self.context_builder.build_aikb_context(aikb_deps)
        schema_data, schema_metrics = self.context_builder.build_schema_context(schema_deps)
        
        context_vars.aikb = aikb_data
        context_vars.schemas = schema_data

        # 4. Load Template
        filename = prompt_config["filename"]
        template_str, template_hit = self._read_template_file(filename)

        # 5. Render Template via Engine
        # We convert the entire PromptContext Pydantic model to a dict for Jinja2
        render_dict = context_vars.model_dump()
        if "variables" in render_dict and isinstance(render_dict["variables"], dict):
            render_dict.update(render_dict["variables"])
        rendered_text = self.template_engine.render(template_str, render_dict)

        # 6. Observability and Size Estimation
        chars = len(rendered_text)
        words = len(rendered_text.split())
        est_tokens = int(chars / RuntimeConfig.CHARS_PER_TOKEN)
        
        if est_tokens > RuntimeConfig.MAX_TOKENS_WARNING:
            warnings.warn(f"Rendered prompt exceeds token warning limit ({est_tokens} > {RuntimeConfig.MAX_TOKENS_WARNING})", OversizedPromptWarning)

        total_hits = aikb_metrics["hits"] + schema_metrics["hits"] + (1 if template_hit else 0)
        total_misses = aikb_metrics["misses"] + schema_metrics["misses"] + (0 if template_hit else 1)
        render_time_ms = (time.time() - start_time) * 1000

        metadata = RuntimeMetadata(
            render_time_ms=render_time_ms,
            cache_hits=total_hits,
            cache_misses=total_misses,
            prompt_size_chars=chars,
            prompt_size_words=words,
            estimated_tokens=est_tokens,
            template_version=version,
            knowledge_version=context_vars.knowledge_version
        )

        return PromptRequest(
            rendered_text=rendered_text,
            metadata=metadata,
            request_id=context_vars.request_id
        )
