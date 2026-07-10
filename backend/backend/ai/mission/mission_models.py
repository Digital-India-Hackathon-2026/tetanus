from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any

class MissionMetadata(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    aikb_version: str
    schema_version: str
    generated_at: str
    mission_hash: str
    source: str
    loaded_from: str
    load_time_ms: float

class MissionContext(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    mission: str
    supported: bool
    definition: Dict[str, Any]
    primary_categories: List[str]
    secondary_categories: List[str]
    required_categories: List[str]
    optional_categories: List[str]
    category_weights: Dict[str, float]
    bundle_ids: List[str]
    priority: str
    mission_type: str
    metadata: MissionMetadata
