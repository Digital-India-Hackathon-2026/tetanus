from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import time

class RuntimeMetadata(BaseModel):
    """Captures observability metrics for a specific prompt render execution."""
    render_time_ms: float
    cache_hits: int = 0
    cache_misses: int = 0
    prompt_size_chars: int
    prompt_size_words: int
    estimated_tokens: int
    template_version: str
    knowledge_version: str
    
class PromptContext(BaseModel):
    """The complete context object passed into the template engine."""
    user_input: str
    runtime_metadata: Dict[str, Any] = Field(default_factory=dict)
    knowledge_version: str
    prompt_version: str
    schema_version: str
    request_id: str
    session_id: Optional[str] = None
    language: str = "en"
    country: str = "IN"
    timestamp: float = Field(default_factory=time.time)
    
    # Dynamic variables from AIKB and Schemas will be added as dictionaries during runtime
    aikb: Dict[str, Any] = Field(default_factory=dict)
    schemas: Dict[str, Any] = Field(default_factory=dict)
    variables: Dict[str, Any] = Field(default_factory=dict)

class PromptRequest(BaseModel):
    """The final strictly rendered prompt payload intended for Gemini."""
    rendered_text: str
    metadata: RuntimeMetadata
    request_id: str
