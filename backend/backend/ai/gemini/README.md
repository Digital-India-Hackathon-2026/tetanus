# Gemini Infrastructure Module

This module provides a robust, strictly decoupled, and production-grade client for Google's Gemini API using the `google-genai` SDK.

## Responsibilities
- **Asynchronous Execution:** Integrates seamlessly with FastAPI via `async/await`.
- **Fault Tolerance:** Implements exponential backoff for `RateLimitError` (429) and `TimeoutError` using `tenacity`.
- **Concurrency Control:** Limits parallel requests via `asyncio.Semaphore` to avoid overwhelming the API.
- **Telemetry:** Logs standardized JSON telemetry including latency, token usage, retry counts, and request IDs.
- **Prompt Loading:** Provides a `PromptLoader` to read markdown/txt prompts from disk.
- **Strong Typing:** Returns structured `GeminiResponse` objects containing usage metadata and finish reasons.

## Separation of Concerns
**IMPORTANT:** This module must NEVER contain business logic, shopping data, or schema definitions. It must remain purely an API transport and orchestration layer.

## How to Use

```python
import asyncio
from backend.ai.gemini import GeminiClient, GeminiModel

async def main():
    client = GeminiClient()
    response = await client.generate_content(
        prompt="Explain quantum physics in one sentence.",
        model=GeminiModel.GEMINI_2_5_FLASH,
        temperature=0.7
    )
    
    print(response.text)
    print(response.usage.total_tokens)
    print(response.latency)

asyncio.run(main())
```

## How NOT to Use
- Do NOT import `backend.ai.schemas` in this module.
- Do NOT hardcode prompts into this module.
- Do NOT parse JSON strings in this module (leave schema enforcement to Pydantic and the Agent layer).
