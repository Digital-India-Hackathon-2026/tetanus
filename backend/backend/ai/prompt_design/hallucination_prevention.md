# Hallucination Prevention

Gemini LLMs are prone to hallucinating products and categories outside the database. 

## What Must Never Be Hallucinated
1.  **Products**: Never recommend a product name that is not explicitly in the Explanation Agent's input payload.
2.  **Categories**: Only emit categories from `supported_categories.json`.
3.  **Brands**: Only emit brands from `supported_brands.json`.
4.  **Missions**: Only emit missions from `mission_catalog.json`.

## Prompt Strategies
1.  **Strict Enum Binding**: The prompt system prompt MUST contain the exact string list of allowed categories/missions.
2.  **Explicit Prohibition Clause**: "UNDER NO CIRCUMSTANCES should you output a category not in the provided ALLOWED_CATEGORIES list."
3.  **Grounding Constraint**: "Your output will be parsed by a strict JSON validation system. If you hallucinate an Enum value, the system will crash."
