from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Any, Optional

class CandidateProduct(BaseModel):
    product_id: str
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    price: float
    mrp: Optional[float] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    inventory: Optional[int] = None
    quality_score: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    mission_score: float = 0.0
    category_score: float = 0.0
    budget_score: float = 0.0
    final_score: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RecommendationContext(BaseModel):
    budget: Optional[float] = None
    preferred_brands: List[str] = Field(default_factory=list)
    excluded_brands: List[str] = Field(default_factory=list)
    urgency: str = "normal"
    preferred_price_range: Optional[str] = None
    inventory_required: str = "in_stock"

from backend.ai.recommendation.ranking.ranking_models import ScoredProduct

class RecommendedProduct(BaseModel):
    product: ScoredProduct
    justification: str = ""

class RecommendedBundle(BaseModel):
    bundle_id: str
    name: str
    products: List[RecommendedProduct]
    total_price: float
    bundle_score: float
    budget_utilization: float = 0.0
    completeness: float = 0.0
    missing_categories: List[str] = Field(default_factory=list)
    missing_products: List[str] = Field(default_factory=list)
    
    # New Readiness Fields
    readiness_score: float = 0.0
    essential_items_found: List[str] = Field(default_factory=list)
    essential_items_missing: List[str] = Field(default_factory=list)
    optional_items_found: List[str] = Field(default_factory=list)
    optional_items_missing: List[str] = Field(default_factory=list)
    completion_percentage: float = 0.0
    estimated_remaining_cost: float = 0.0

class RetrievalStatistics(BaseModel):
    retrieved_count: int = 0
    filtered_count: int = 0
    returned_count: int = 0

class RecommendationMetadata(BaseModel):
    execution_time_ms: float = 0.0
    ranking_time_ms: float = 0.0
    filter_time_ms: float = 0.0
    bundle_time_ms: float = 0.0
    repository_time_ms: float = 0.0

class RecommendationResponse(BaseModel):
    mission: str
    products: List[RecommendedProduct] = Field(default_factory=list)
    bundles: List[RecommendedBundle] = Field(default_factory=list)
    explanation: str = ""
    statistics: RetrievalStatistics = Field(default_factory=RetrievalStatistics)
    metadata: RecommendationMetadata = Field(default_factory=RecommendationMetadata)
    filtering_summary: Dict[str, Any] = Field(default_factory=dict)
    ranking_summary: Dict[str, Any] = Field(default_factory=dict)
    diversity_summary: Dict[str, Any] = Field(default_factory=dict)
