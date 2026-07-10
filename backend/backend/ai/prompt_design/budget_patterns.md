# Budget Normalization Rules

Users express financial constraints in highly varied, qualitative, and qualitative formats. The prompt must extract these into the strict `Budget` JSON schema.

## Quantitative Expressions
*   **Exact**: "₹5000", "5000 rs", "5k" -> `amount: 5000`, `minimum: null`, `maximum: 5000`.
*   **Ceiling**: "Under ₹10000", "Max 10k", "Below 2k" -> `amount: null`, `maximum: 10000`.
*   **Floor**: "At least 1000", "Starting from 5k" -> `amount: null`, `minimum: 1000`.
*   **Range**: "Between 10k and 20k", "10-20 thousand" -> `minimum: 10000`, `maximum: 20000`.
*   **Approximate**: "Around 10k", "Nearly 5k", "Approximately 2000" -> `amount: 10000`, `estimated: true`.

## Qualitative Expressions
*   **Value-focused**: "Value for money", "Best value", "Affordable", "Cheap", "Cheapest"
    *   *Rule*: `maximum` set to median category price; `estimated: true`.
*   **Premium**: "Premium", "Luxury", "High-end", "Best quality"
    *   *Rule*: `minimum` set to 75th percentile category price; `estimated: true`.
*   **Unbounded**: "No budget", "Budget flexible", "Money is no object"
    *   *Rule*: `amount: null`, `minimum: null`, `maximum: null`, `estimated: false`.
