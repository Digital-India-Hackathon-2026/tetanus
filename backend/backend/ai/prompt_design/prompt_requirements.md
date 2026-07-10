# Prompt Requirements Specification

This document outlines the core operational requirements for the Gemini Intent and Explanation Agents. It defines the rigid boundaries between expected AI behavior and prohibited actions.

## 1. What Gemini Needs to Know
*   **Mission Catalog**: Gemini must know the exact subset of supported missions (e.g., Birthday, Gym, Hostel Setup).
*   **Category Constraints**: Gemini must restrict product mapping to only valid categories (e.g., Automotive, Beauty, Electronics).
*   **Schema Output**: The prompt must strictly enforce the `IntentResponse` JSON schema, guaranteeing standard datatypes.
*   **Inventory Rules**: Gemini must map user urgency to inventory status constraints (e.g., "Need it today" -> `IN_STOCK`).

## 2. What Gemini Must Never Do
*   **Invent Missions**: Never synthesize missions outside the provided catalog.
*   **Invent Categories**: Never classify an item into a category that does not exist in `supported_categories.json`.
*   **Generate SQL/Cypher**: Gemini must output structured JSON parameters, never direct database queries.
*   **Violate Budgets**: Never recommend a bundle whose estimated price strictly exceeds a user's hard maximum cap.
*   **Return Malformed JSON**: Never wrap the JSON response in markdown code blocks or conversational text.

## 3. What Gemini Should Infer
*   **Implicit Missions**: When a user says "I am moving out", infer the related setup mission.
*   **Price Tiers**: If a user says "premium", infer `preferred_price_range = "premium"` and adjust category budgets.
*   **Urgency**: If a user says "ASAP", infer `maximum_delivery_days = 1`.

## 4. What Gemini Should Ignore
*   **Conversational Fluff**: Greetings, polite phrasing, and off-topic commentary.
*   **Unsupported Demands**: e.g., "Recommend a restaurant nearby" -> Should be safely ignored or handled via fallback.

## 5. What Gemini Should Validate
*   **Confidence Calculation**: Every extracted mission, budget, and constraint requires a mathematically sound confidence score based on the explicitness of the user's request.
