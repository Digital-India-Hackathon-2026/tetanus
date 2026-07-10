from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from .types import Mission, Category, Currency, InventoryStatus, QuestionType, QuestionID, UrgencyLevel, IntentStatus

class Budget(BaseModel):
    """Schema defining user budget parameters."""
    amount: Optional[float] = Field(None, description="Exact budget amount if specified")
    currency: Currency = Field(default=Currency.INR, description="Currency of the budget")
    minimum: Optional[float] = Field(None, description="Minimum acceptable price")
    maximum: Optional[float] = Field(None, description="Maximum acceptable price")
    estimated: Optional[bool] = Field(False, description="Whether the budget is an AI estimation")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Confidence in the budget extraction")

class Constraint(BaseModel):
    """Schema defining user constraints and preferences."""
    preferred_brands: List[str] = Field(default_factory=list, description="List of specifically requested brands")
    excluded_brands: List[str] = Field(default_factory=list, description="Brands the user does not want")
    preferred_categories: List[Category] = Field(default_factory=list, description="Categories the user is interested in")
    must_have: List[str] = Field(default_factory=list, description="Features or keywords the items MUST have")
    nice_to_have: List[str] = Field(default_factory=list, description="Features or keywords the user would like")
    maximum_delivery_days: Optional[int] = Field(None, description="Maximum acceptable delivery time in days")
    preferred_price_range: Optional[str] = Field(None, description="Qualitative price range e.g., 'cheap', 'premium'")
    minimum_rating: float = Field(0.0, ge=0.0, le=5.0, description="Minimum acceptable average rating")
    inventory_required: InventoryStatus = Field(default=InventoryStatus.IN_STOCK, description="Required inventory status")
    urgency: UrgencyLevel = Field(default=UrgencyLevel.NORMAL, description="Urgency of the request")

class ClarificationQuestion(BaseModel):
    """Schema for a single clarification question."""
    id: QuestionID = Field(..., description="Unique identifier for the clarification prompt")
    question: str = Field(..., description="Natural language question to present to the user")
    type: QuestionType = Field(..., description="Structured selection or input type")
    options: List[str] = Field(default_factory=list, description="Selection options if single/multi-select")

class Metadata(BaseModel):
    """Metadata tracking request properties."""
    language: str = Field(default="en", description="Language code of the request")
    country: str = Field(default="IN", description="Country code of the user")
    currency: Currency = Field(default=Currency.INR, description="Requested currency")
    timestamp: str = Field(..., description="ISO8601 timestamp of the request")
    model_version: str = Field(..., description="Version of the Gemini model used")
    knowledge_base_version: str = Field(..., description="Version of the AIKB used")
    request_id: str = Field(..., description="Unique UUID for tracing the request")
    session_id: Optional[str] = Field(None, description="Active session ID")
    intent_version: str = Field(default="v1", description="Version of the Intent Agent prompt")
    stage: str = Field(default="intent_extraction", description="Pipeline stage of the output")
    prompt_tokens: Optional[int] = Field(None, description="Prompt tokens used")
    output_tokens: Optional[int] = Field(None, description="Output tokens generated")
    latency_ms: Optional[float] = Field(None, description="Latency in milliseconds")

class IntentResponse(BaseModel):
    """Master schema for the Intent Agent output."""
    model_config = ConfigDict(title="IntentResponse", extra="forbid")
    intent_status: IntentStatus = Field(..., description="Status of the intent resolution")
    primary_mission: Optional[str] = Field(None, description="The primary mission identified from the catalog")
    secondary_missions: List[str] = Field(default_factory=list, description="Any secondary missions identified")
    overall_confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence of the intent extraction")
    confidence_breakdown: Optional[Dict[str, float]] = Field(None, description="Optional breakdown of confidence scores")
    categories: List[Category] = Field(default_factory=list, description="Categories relevant to the request")
    keywords: List[str] = Field(default_factory=list, description="Extracted keywords mapping to the AIKB")
    budget: Budget = Field(..., description="Extracted or inferred budget")
    constraints: Constraint = Field(..., description="User constraints and preferences")
    reasoning_summary: Optional[str] = Field(None, description="Concise 1-2 sentence summary of reasoning")
    needs_clarification: bool = Field(default=False, description="Whether clarification is required before recommendations")
    questions: List[ClarificationQuestion] = Field(default_factory=list, description="Clarification questions if needs_clarification is True")
    request_metadata: Metadata = Field(..., description="Metadata for logging and tracking")

class ExplanationResponse(BaseModel):
    """Master schema for the Explanation Agent output."""
    mission: str = Field(..., description="The mission context for the explanation")
    recommended_products: List[str] = Field(..., description="List of recommended product names")
    recommendation_reasons: dict[str, str] = Field(..., description="Dictionary mapping product names to explanation strings")
    bundles: List[str] = Field(default_factory=list, description="List of recommended bundle names")
    budget_summary: str = Field(..., description="Explanation of how the recommendations fit the budget")
    inventory_summary: str = Field(..., description="Summary of inventory status for the recommendations")
    alternative_products: List[str] = Field(default_factory=list, description="List of alternative product names")

class ClarificationResponse(BaseModel):
    """Output from the Clarification Engine specifying if and what questions to ask."""
    needs_clarification: bool = Field(..., description="Whether the user needs to be asked clarification questions")
    questions: List[ClarificationQuestion] = Field(default_factory=list, description="List of questions to ask, in priority order")
    reason: Optional[str] = Field(None, description="Internal reasoning for why clarification was triggered")
    clarification_version: str = Field(default="v1", description="Version of the clarification engine logic")
