import time
import uuid
import asyncio
from typing import Optional, Dict, Any
from google import genai
from google.genai import types

from .config import GeminiConfig
from .logger import GeminiLogger
from .exceptions import AuthenticationError, RateLimitError, TimeoutError, InvalidResponseError, GeminiAPIError
from .usage import Usage, GeminiResponse
from .response_parser import GeminiResponseParser
from .rate_limiter import global_rate_limiter
from .retry import with_retry

class GeminiClient:
    """
    Reusable, domain-agnostic asynchronous Gemini client.
    Handles configuration, rate-limiting, retries, and telemetry logging.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GeminiConfig.API_KEY
        if not self.api_key:
            raise AuthenticationError("No API key provided. Set GEMINI_API_KEY environment variable.")
            
        # Initialize the new google-genai SDK client
        self.client = genai.Client(api_key=self.api_key)
        self.logger = GeminiLogger()

    @with_retry()
    async def _execute_with_retry(self, model: str, contents: Any, config: types.GenerateContentConfig, request_id: str, session_id: Optional[str]) -> GeminiResponse:
        """Internal execution wrapper that triggers tenacity retries on specific exceptions."""
        try:
            start_time = time.time()
            client = genai.Client(api_key=self.api_key)
            # Await the async model generation
            response = await client.aio.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
            latency_ms = (time.time() - start_time) * 1000

            # Parse and structure usage
            usage = Usage(
                prompt_tokens=response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                response_tokens=response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                total_tokens=response.usage_metadata.total_token_count if response.usage_metadata else 0,
                latency_ms=latency_ms
            )

            # Extract raw text
            text = GeminiResponseParser.parse_text(response)
            
            # Determine finish reason
            finish_reason = None
            if response.candidates and len(response.candidates) > 0:
                # In google-genai, finish_reason is an enum/string
                finish_reason = str(response.candidates[0].finish_reason)

            # Log success
            self.logger.log_success(request_id=request_id, latency_ms=latency_ms, usage=usage)

            return GeminiResponse(
                text=text,
                usage=usage,
                latency=latency_ms,
                model=model,
                finish_reason=finish_reason,
                raw_response=response
            )

        except Exception as e:
            # Map google-genai exceptions to our custom hierarchy
            err_str = str(e).lower()
            if "429" in err_str or "quota" in err_str:
                self.logger.log_retry(request_id, 0, e) # Basic logging, tenacity handles actual retry count
                raise RateLimitError(f"Rate limit exceeded: {str(e)}")
            elif "401" in err_str or "403" in err_str or "api key" in err_str:
                raise AuthenticationError(f"Authentication failed: {str(e)}")
            elif "timeout" in err_str:
                self.logger.log_retry(request_id, 0, e)
                raise TimeoutError(f"Request timed out: {str(e)}")
            elif isinstance(e, InvalidResponseError):
                raise
            else:
                raise GeminiAPIError(f"Unexpected API error: {str(e)}")

    _cache: Dict[str, GeminiResponse] = {}

    async def generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        session_id: Optional[str] = None,
        prompt_version: Optional[str] = None,
        knowledge_base_version: Optional[str] = None,
        response_schema: Optional[Any] = None,
        response_mime_type: Optional[str] = None,
        cache_key: Optional[str] = None,
        fallback_text: Optional[str] = None
    ) -> GeminiResponse:
        """
        Primary interface for content generation.
        """
        if cache_key and cache_key in self._cache:
            return self._cache[cache_key]

        request_id = str(uuid.uuid4())
        model_name = model or GeminiConfig.DEFAULT_MODEL
        
        self.logger.log_request(
            request_id=request_id,
            session_id=session_id,
            model=model_name,
            prompt_version=prompt_version,
            knowledge_base_version=knowledge_base_version
        )

        config_kwargs = {
            "temperature": temperature if temperature is not None else GeminiConfig.DEFAULT_TEMPERATURE,
            "max_output_tokens": max_tokens if max_tokens is not None else GeminiConfig.DEFAULT_MAX_TOKENS,
            "top_p": top_p if top_p is not None else GeminiConfig.DEFAULT_TOP_P,
            "top_k": top_k if top_k is not None else GeminiConfig.DEFAULT_TOP_K,
        }
        
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction
            
        if response_schema:
            config_kwargs["response_schema"] = response_schema
            
        if response_mime_type:
            config_kwargs["response_mime_type"] = response_mime_type
            
        config = types.GenerateContentConfig(**config_kwargs)

        # Apply rate limiter
        await global_rate_limiter.acquire()
        try:
            response = await self._execute_with_retry(
                model=model_name,
                contents=prompt,
                config=config,
                request_id=request_id,
                session_id=session_id
            )
            
            # JSON markdown stripping
            if response_mime_type == "application/json" and response.text:
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text[7:]
                elif text.startswith("```"):
                    text = text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                response.text = text.strip()
                
            if cache_key:
                self._cache[cache_key] = response
            return response
        except Exception as e:
            self.logger.log_failure(request_id, e)
            if fallback_text is not None:
                return GeminiResponse(
                    text=fallback_text,
                    usage=Usage(prompt_tokens=0, response_tokens=0, total_tokens=0, latency_ms=0),
                    latency=0.0,
                    model=model_name,
                    finish_reason="fallback",
                    raw_response=None
                )
            raise
        finally:
            global_rate_limiter.release()
