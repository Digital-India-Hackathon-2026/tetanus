class GeminiAPIError(Exception):
    """Base exception for all Gemini API errors."""
    pass

class AuthenticationError(GeminiAPIError):
    """Raised when the API key is missing or invalid."""
    pass

class RateLimitError(GeminiAPIError):
    """Raised when the API returns a 429 Too Many Requests."""
    pass

class TimeoutError(GeminiAPIError):
    """Raised when the API request times out."""
    pass

class InvalidResponseError(GeminiAPIError):
    """Raised when the response is empty, malformed, or cannot be parsed."""
    pass

class RetryLimitExceeded(GeminiAPIError):
    """Raised when all retry attempts for a request have failed."""
    pass
