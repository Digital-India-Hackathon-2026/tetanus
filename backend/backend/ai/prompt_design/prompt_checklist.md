# Prompt Deployment Checklist

Before any Gemini prompt is deployed to production, it must pass this manual verification checklist:

- [ ] Does the system prompt inject the `Category` enum dynamically?
- [ ] Does the system prompt inject the `Mission` enum dynamically?
- [ ] Are JSON schema instructions explicitly provided with examples?
- [ ] Does the prompt explicitly ban conversational prefixes (e.g., "Here is your JSON:")?
- [ ] Are Indian English abbreviations (PG, Engg) explicitly mentioned as context?
- [ ] Are budget normalization instructions provided (e.g. how to handle "Cheap")?
- [ ] Are the confidence calculation rules clearly defined?
- [ ] Does the prompt explicitly handle impossible edge cases (e.g., zero budget)?
