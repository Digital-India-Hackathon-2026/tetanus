class RecommendationConfig:
    def __init__(self):
        self.max_candidates = 100
        self.max_returned_products = 10
        self.max_returned_bundles = 3
        
        # Intent Bonus Scorer configuration (per-mission)
        self.intent_bonus_scores = {
            "hostel setup": {"bonus": 0.18},
            "travel": {"bonus": 0.12},
            "gym": {"bonus": 0.16},
            "work from home": {"bonus": 0.15},
            "movie night": {"bonus": 0.10},
            "birthday party": {"bonus": 0.14},
            "gaming setup": {"bonus": 0.15},
            "college essentials": {"bonus": 0.12}
        }
        self.default_intent_bonus = 0.10
        
        # Bundle Readiness configuration
        self.default_fallback_price = 500.0
