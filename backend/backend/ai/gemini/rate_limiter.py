import asyncio
from .config import GeminiConfig

class RateLimiter:
    """Asynchronous rate limiter to prevent 429 Too Many Requests errors.
    Uses a semaphore to limit concurrent requests.
    """
    def __init__(self, max_concurrent: int = GeminiConfig.MAX_CONCURRENT_REQUESTS):
        self.max_concurrent = max_concurrent
        self._semaphore = None

    @property
    def semaphore(self) -> asyncio.Semaphore:
        """Lazy initialization of semaphore to ensure it's created in the correct event loop."""
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.max_concurrent)
        return self._semaphore

    async def acquire(self):
        """Acquire a token from the rate limiter."""
        await self.semaphore.acquire()

    def release(self):
        """Release a token back to the rate limiter."""
        if self._semaphore:
            self._semaphore.release()

# Global rate limiter instance
global_rate_limiter = RateLimiter()
