# Prompt Runtime Engine

This subsystem is purely responsible for safely combining static templates with dynamic user input, schemas, and AI Knowledge Base JSON into a final prompt payload for Gemini.

## Responsibilities
- **Template Rendering:** Uses Jinja2 with strict validation (missing variables crash the request).
- **Caching:** Prevents repetitive disk reading of JSON files and templates via `MemoryCache`.
- **Validation:** Ensures dependencies in `prompt_manifest.json` are loaded appropriately.
- **Metrics:** Tracks cache hits, misses, render times, and approximate token counts for observability.

## Architecture
1. **Manifest Validation:** Ensures requested prompt and version exist.
2. **Context Builder:** Plucks only requested schemas and AIKB arrays out of cache.
3. **Template Engine:** Substitutes the variables securely.

## How to use

```python
from backend.ai.runtime import PromptRenderer, PromptContext

renderer = PromptRenderer()

context = PromptContext(
    user_input="I need a laptop for college",
    knowledge_version="current",
    prompt_version="v1",
    schema_version="v1",
    request_id="req-123",
    variables={}
)

request = renderer.render("intent_extraction", "v1", context)

print(request.rendered_text)
print(request.metadata.cache_hits)
```
