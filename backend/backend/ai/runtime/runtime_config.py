import os
from pathlib import Path

class RuntimeConfig:
    """Configuration for the Prompt Runtime Engine."""
    
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    
    # Core directories
    PROMPTS_DIR = BASE_DIR / "backend" / "ai" / "prompts"
    KNOWLEDGE_DIR = BASE_DIR / "backend" / "ai" / "knowledge" / "current"
    SCHEMAS_DIR = BASE_DIR / "backend" / "ai" / "schemas"
    
    # Prompt Size Limits
    MAX_TOKENS_WARNING = int(os.getenv("PROMPT_MAX_TOKENS_WARNING", "4000"))
    CHARS_PER_TOKEN = 4.0  # Industry standard estimation
    
    # Cache Configuration
    CACHE_TTL_SECONDS = int(os.getenv("PROMPT_CACHE_TTL", "3600"))
