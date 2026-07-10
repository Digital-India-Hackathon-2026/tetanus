import time
from typing import Dict, Any
from .client import GeminiClient
from .exceptions import GeminiAPIError
from .config import GeminiConfig

async def check_gemini_connection() -> Dict[str, Any]:
    """
    Verifies API connectivity, validates credentials, and measures latency.
    Useful for system health checks.
    """
    try:
        client = GeminiClient()
        start_time = time.time()
        
        # We send a trivial prompt just to test connectivity
        response = await client.generate_content(
            prompt="Reply with the single word 'OK'.",
            max_tokens=5,
            temperature=0.0
        )
        
        latency_ms = (time.time() - start_time) * 1000
        
        return {
            "status": "connected",
            "model": response.model,
            "latency_ms": round(latency_ms, 2),
            "auth": "valid"
        }
    except GeminiAPIError as e:
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "message": str(e),
            "auth": "invalid" if "AuthenticationError" in type(e).__name__ else "unknown"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_type": "Unknown",
            "message": str(e),
            "auth": "unknown"
        }
