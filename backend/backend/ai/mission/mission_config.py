from typing import List, Dict

# Keywords that short-circuit the pipeline immediately
UNSUPPORTED_KEYWORDS: List[str] = [
    "flight", "hotel", "passport", "visa", "motorcycle", "car", "loan", 
    "insurance", "doctor", "cancer", "real estate", "stocks", "crypto", 
    "mutual funds", "investment", "bitcoin", "ticket", "surgery"
]

# Mapping of raw or hallucinated categories to graph taxonomy
CATEGORY_MAPPINGS: Dict[str, List[str]] = {
    "bedroom": ["Home"],
    "kitchenware": ["Kitchen"],
    "kitchen": ["Kitchen"],
    "fitness": ["Sports"],
    "running": ["Sports"],
    "sportswear": ["Fashion", "Sports"],
    "home decor": ["Home"],
    "electronics accessories": ["Electronics"],
    "office equipment": ["Office"],
    "personal care": ["Beauty"],
    "health": ["Beauty"] # Health sometimes falls under Beauty/Wellness
}

def normalize_categories(categories: List[str]) -> List[str]:
    """Normalizes a list of categories using deterministic mappings."""
    normalized = []
    for cat in categories:
        cat_lower = cat.lower().strip()
        if cat_lower in CATEGORY_MAPPINGS:
            normalized.extend(CATEGORY_MAPPINGS[cat_lower])
        else:
            # Capitalize the first letter (e.g. "home" -> "Home") to try to match graph taxonomy
            normalized.append(cat.title())
    # Deduplicate while preserving order
    return list(dict.fromkeys(normalized))
