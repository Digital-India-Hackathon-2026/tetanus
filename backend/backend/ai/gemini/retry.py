from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import logging
from .exceptions import RateLimitError, TimeoutError, GeminiAPIError
from .config import GeminiConfig

retry_logger = logging.getLogger("GeminiRetry")

def with_retry():
    """
    Decorator for wrapping Gemini API calls with exponential backoff.
    Only retries on RateLimitError and TimeoutError.
    """
    return retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=10, max=30),
        retry=retry_if_exception_type((RateLimitError, TimeoutError)),
        before_sleep=before_sleep_log(retry_logger, logging.WARNING),
        reraise=True
    )
