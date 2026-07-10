from typing import List
from abc import ABC, abstractmethod
from backend.ai.recommendation.models import CandidateProduct, RecommendedBundle
from backend.ai.mission.mission_models import MissionContext

class BundleBuilderInterface(ABC):
    @abstractmethod
    def build_bundles(self, products: List[CandidateProduct], context: MissionContext) -> List[RecommendedBundle]:
        pass
