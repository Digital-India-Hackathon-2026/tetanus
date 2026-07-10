# Ranking Engine

Phase 7.3 of the Recommendation Pipeline. Assigns deterministic scores to filtered candidate products using a fully configuration-driven, multi-profile engine.

## Architecture

```
CandidateProduct[] + MissionContext + RecommendationContext
    ↓
ScorerRegistry (loads scorers from ranking_config.json profile)
    ↓  7 parallel scorers
  base_score = sum(weighted_score per scorer), clamped [0,1]
    ↓
BoostEngine (additive, clamped to 1.0)
    ↓
PenaltyEngine (additive deductions, clamped to 0.0)
    ↓
RankingReasonBuilder (derives top 5 deterministic reasons)
    ↓
ScoredProduct[] (sorted descending) + RankingReport
```

## Scorer Pipeline (7 Scorers)

| Scorer                | Weight (balanced) | Normalization         |
|-----------------------|-------------------|-----------------------|
| MissionMatchScorer    | 0.35              | Primary=1.0, Secondary=0.65 |
| BudgetScorer          | 0.20              | Smooth quadratic curve|
| QualityScorer         | 0.15              | Linear 0-10 → 0-1     |
| RatingScorer          | 0.10              | Linear 0-5 → 0-1      |
| ReviewScorer          | 0.05              | log1p(count)/log1p(scale) |
| BrandScorer           | 0.10              | 0.0/0.5/1.0 (none/neutral/preferred) |
| CategoryPriorityScorer| 0.05              | From category_weights |

## Ranking Profiles

Four built-in profiles in `ranking_config.json`:
- **balanced**: Equal emphasis across all dimensions.
- **budget_first**: Budget proximity is the dominant signal (weight=0.40).
- **quality_first**: Quality score and rating dominate (weight=0.30).
- **premium**: Brand/quality/review count matters most, budget is largely ignored.

Select a profile at runtime: `RankingEngine(profile="budget_first")`

## Adding a New Scorer

1. Create a class that extends `BaseScorer`.
2. Decorate it with `@ScorerRegistry.register("your_scorer_key")`.
3. Implement `score(product, mission_context, recommendation_context, config) -> ScoringResult`.
4. Add `your_scorer_key` to each profile's `weights` dict in `ranking_config.json`.
5. The engine will automatically discover and load it.

## Immutability Guarantee

`CandidateProduct` instances are **never mutated**. All scoring data is stored in the `ScoredProduct` wrapper's `score_breakdown` field.
