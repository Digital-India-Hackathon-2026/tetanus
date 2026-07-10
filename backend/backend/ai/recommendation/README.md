# Recommendation Pipeline

The Recommendation Pipeline is a fully deterministic, modular system designed to retrieve, filter, rank, diversify, and bundle products based on a `MissionContext`. 

## Design Principles
- **No LLM Reasoning**: All recommendations are derived from structured data and rules, without relying on prompt engineering or generative AI.
- **Single Responsibility**: Each layer in the pipeline is isolated.
- **Orchestration Only**: The `RecommendationService` coordinates the layers but contains no business logic.

## Pipeline Architecture
1. **Retrieval**: Adapters for Graph (Neo4j) and Relational (PostgreSQL) databases.
2. **Filtering**: Removes products based on hard constraints (budget, exclusions).
3. **Ranking**: Applies scoring rules to sort candidates.
4. **Diversity**: Ensures the final result isn't flooded with similar items.
5. **Bundling**: Packages top items into thematic bundles based on the mission.

## Retrieval & Repository Layer
### Connection Lifecycle
The Neo4j driver uses connection pooling by default. Connections are initialized on first access, verified via `health_check()`, and automatically released back to the pool. Ensure `.env` is populated with `NEO4J_URI`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD`.

### Cypher Organization
All Cypher queries are strictly sequestered in `graph_queries.py` as string constants. No inline Cypher exists in the repository logic.

### Mapping Layer
Raw Neo4j records are immediately transformed into immutable `CandidateProduct` Pydantic models. Any missing required properties during extraction throw a `RetrievalError`.

## Future Implementations
- Relational retrieval via `PostgresRepository`.
- Active recommendation algorithms across filtering, ranking, diversity, and bundling.

### Future Relationships
To support complex recommendation features, the Neo4j schema is expected to expand with:
- `[:SIMILAR_TO]`
- `[:COMPLEMENTS]`
- `[:ALTERNATIVE_TO]`
- `[:FREQUENTLY_BOUGHT_WITH]`

These are **NOT** implemented yet but have stubbed interfaces in `GraphRepositoryInterface`.
