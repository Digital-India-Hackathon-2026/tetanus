import logging
import json
import time
from typing import Optional, Dict, Any

# Configure standard logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

class GeminiLogger:
    """Structured logger for Gemini API operations."""

    def __init__(self, name: str = "GeminiClient"):
        self.logger = logging.getLogger(name)

    def log_request(self, request_id: str, session_id: Optional[str], model: str, prompt_version: Optional[str] = None, knowledge_base_version: Optional[str] = None):
        """Log an outgoing request."""
        self.logger.info(
            f"Outgoing Request | ReqID: {request_id} | Session: {session_id} | Model: {model} | PromptV: {prompt_version} | KBV: {knowledge_base_version}"
        )

    def log_success(self, request_id: str, latency_ms: float, usage: Any, retry_count: int = 0):
        """Log a successful response."""
        prompt_tokens = getattr(usage, "prompt_tokens", 0)
        response_tokens = getattr(usage, "response_tokens", 0)
        self.logger.info(
            f"Success | ReqID: {request_id} | Latency: {latency_ms:.2f}ms | Retries: {retry_count} | Tokens: (In: {prompt_tokens}, Out: {response_tokens})"
        )

    def log_failure(self, request_id: str, error: Exception, retry_count: int = 0):
        """Log a failure."""
        self.logger.error(
            f"Failure | ReqID: {request_id} | Retries: {retry_count} | Error: {type(error).__name__} - {str(error)}"
        )
        
    def log_retry(self, request_id: str, attempt: int, error: Exception):
        """Log a retry attempt."""
        self.logger.warning(
            f"Retry Attempt | ReqID: {request_id} | Attempt: {attempt} | Caused by: {type(error).__name__}"
        )
