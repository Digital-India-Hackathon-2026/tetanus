from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ScoreComponent(BaseModel):
    scorer_name: str
    raw_score: float
    weighted_score: float
    weight: float
    explanation: str


class AppliedBoost(BaseModel):
    boost_name: str
    boost_value: float
    reason: str


class AppliedPenalty(BaseModel):
    penalty_name: str
    penalty_value: float
    reason: str


class ScoreBreakdown(BaseModel):
    base_score: float
    components: List[ScoreComponent] = Field(default_factory=list)
    boosts_applied: List[AppliedBoost] = Field(default_factory=list)
    penalties_applied: List[AppliedPenalty] = Field(default_factory=list)
    after_boost_score: float = 0.0
    final_score: float = 0.0
    top_reasons: List[str] = Field(default_factory=list)


class ScoringResult(BaseModel):
    scorer_name: str
    raw_score: float
    weighted_score: float
    explanation: str


class ScoredProduct(BaseModel):
    product_id: str
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    price: float
    rating: Optional[float] = None
    review_count: Optional[int] = None
    quality_score: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    inventory: Optional[int] = None
    score_breakdown: ScoreBreakdown = Field(default_factory=ScoreBreakdown)
    final_score: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PerScorerTelemetry(BaseModel):
    scorer_name: str
    execution_time_ms: float
    average_contribution: float


class RankingReport(BaseModel):
    products_ranked: int = 0
    execution_time_ms: float = 0.0
    per_scorer_telemetry: List[PerScorerTelemetry] = Field(default_factory=list)
    top_score: float = 0.0
    lowest_score: float = 0.0
    average_score: float = 0.0
    score_distribution: Dict[str, int] = Field(default_factory=dict)
    profile_used: str = "balanced"
