# Intent Agent Prompts Changelog

## [v1] - Initial Production Refinement
### Added
- Created `rules.md` to extract modular rules (budget, clarification, format).
- Added UrgencyLevel mapping to rules and schema constraints.
- Added `intent_status` classification.
- Added `overall_confidence` and optional breakdown support.

### Changed
- Replaced `id` strings in clarification questions with `QuestionID` enums.
- Reduced examples count: 10 full examples, 20 compact examples.
- Schema explicitly rejects extra keys with Pydantic `extra = "forbid"`.

### Removed
- Removed internal chain of thought (`reasoning`) field to force concise classification.
