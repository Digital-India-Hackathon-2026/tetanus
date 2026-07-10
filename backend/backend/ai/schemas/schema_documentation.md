# AI Contract Schemas Documentation

This directory contains the canonical JSON Schemas and strongly-typed Pydantic models that form the strict API contract between Gemini, FastAPI, and the broader CIN system.

## The Primary Source of Truth
The `models.py` file contains the Pydantic models which act as the absolute source of truth. They dynamically inherit valid enumerations (Missions, Categories) from `types.py`, which is generated directly from the AI Knowledge Base (`backend/ai/knowledge/current/`).

The JSON Schema files (`*_schema.json`) in this directory are automatically generated from these Pydantic models. They follow the JSON Schema 2020-12 specification and are provided for documentation and external interoperability.

## Schemas
*   **Mission Schema / Response Schema**: (`IntentResponse`) Defines the exact structure Gemini must return to classify a user's intent, budget, and constraints.
*   **Explanation Schema**: (`ExplanationResponse`) Defines the structure required by the Explanation Agent to formulate recommendation reasoning.
*   **Budget & Constraint Schemas**: Sub-schemas detailing how to capture financial limits and specific filtering rules (like preferred brands or minimum ratings).

## Validation Rules
All validations are rigidly enforced by Pydantic:
*   `confidence` scores must always be between `0.0` and `1.0`.
*   `minimum_rating` must be between `0.0` and `5.0`.
*   `primary_mission` strictly checks against the `Mission` Enum.
*   `categories` must exist in the `Category` Enum.
*   Required fields cannot be omitted, and types must match exactly (or be safely coercible).

For a complete breakdown, refer to `schema_examples.json`, which documents verified valid and invalid payloads along with explanations for the failures.
