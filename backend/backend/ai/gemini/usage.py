from pydantic import BaseModel
from typing import Optional, Any

class Usage(BaseModel):
    prompt_tokens: int = 0
    response_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0
    cost_estimate: Optional[float] = None

class GeminiResponse(BaseModel):
    text: str
    usage: Usage
    latency: float
    model: str
    finish_reason: Optional[str] = None
    raw_response: Optional[Any] = None
