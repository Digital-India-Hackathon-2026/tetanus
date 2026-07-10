# Filtering Layer

The Filtering Layer is Phase 7.2 of the Recommendation Pipeline. It is purely deterministic and implements a strict "Keep or Remove" policy. 

## Design Principles
- **No LLM/Gemini**: 100% deterministic code.
- **No Database Logic**: Evaluates in-memory `CandidateProduct` objects retrieved by Phase 7.1.
- **No Scoring/Ranking**: It never modifies `CandidateProduct` properties, especially `quality_score`. It only returns a subset of products.
- **Immutability**: Products are treated as immutable within the filter.

## Components

- **`RecommendationContext`**: Encapsulates deterministic constraints parsed from the user's intent (e.g., `budget`, `preferred_brands`, `urgency`). This removes any direct dependency on `IntentResponse` in the recommendation layer.
- **`BaseFilter`**: An abstract base class that ensures all filters conform to the `apply(products, mission_context, recommendation_context, config) -> (kept_products, filter_decisions)` signature.
- **`FilterRegistry`**: Dynamically registers and loads filters.
- **`FilterPipeline`**: Orchestrates the sequential execution of registered filters based on `filter_config.json`.
- **`FilterDecision`**: Represents a dropped product, tracking the filter name, product ID, product name, and the specific reason for removal.
- **`FilterReport`**: Aggregates filtering decisions and per-filter execution telemetry (time, products in/out).

## Execution Order
The execution order is explicitly defined in `filter_config.json`. Typical order:
1. `BudgetFilter`
2. `MissionCategoryFilter`
3. `BrandFilter`
4. `InventoryFilter`
5. `QualityFilter`
6. `DuplicateFilter`
