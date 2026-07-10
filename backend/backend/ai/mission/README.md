# Mission Service

The Mission Service acts as the deterministic bridge between the AI Intent layer and the Recommendation Engine.

## Responsibilities
- Receives `IntentResponse` from the Clarification Engine.
- Dynamically loads and parses deterministic mappings from the AI Knowledge Base (`backend/ai/knowledge/current`).
- Returns an immutable `MissionContext` model to the Recommendation Engine.

## Architecture
- `MissionCache`: Singleton for loading the AIKB once at startup. No TTL. Use `reload()` to refresh.
- `MissionValidator`: Enforces strict consistency and completeness of the AIKB data structure upon load. Fails early.
- `MissionLoader`: Retrieves cache payloads.
- `MissionService`: Main entry point exposing `resolve(intent_response) -> MissionContext`.

## MissionContext
Immutable Pydantic model populated deterministically from the AIKB. Contains categories, weights, bundles, priority, and metadata for a resolved mission.

## How to Add a New Mission
To expand AI reasoning without changing Python code:
1. Update dataset (CSV catalogs or mapping logic).
2. Run `build_aikb.py` to regenerate the JSON files.
3. Restart backend.
