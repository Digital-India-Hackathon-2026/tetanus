from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class FilterDecision(BaseModel):
    filter_name: str
    product_id: str
    product_name: str
    reason: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class PerFilterTelemetry(BaseModel):
    filter_name: str
    execution_time_ms: float
    products_in: int
    products_out: int

class FilterReport(BaseModel):
    input_products: int = 0
    remaining_products: int = 0
    execution_time_ms: float = 0.0
    decisions: List[FilterDecision] = Field(default_factory=list)
    telemetry: List[PerFilterTelemetry] = Field(default_factory=list)
