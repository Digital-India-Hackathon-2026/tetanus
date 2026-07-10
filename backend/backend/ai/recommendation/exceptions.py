class RecommendationError(Exception):
    pass

class RetrievalError(RecommendationError):
    pass

class FilteringError(RecommendationError):
    pass

class RankingError(RecommendationError):
    pass

class BundleError(RecommendationError):
    pass

class RepositoryError(Exception):
    pass
