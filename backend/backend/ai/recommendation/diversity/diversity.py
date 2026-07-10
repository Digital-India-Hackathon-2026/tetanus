from typing import List
from abc import ABC, abstractmethod
from backend.ai.recommendation.models import CandidateProduct
from backend.ai.mission.mission_models import MissionContext

class DiversityInterface(ABC):
    @abstractmethod
    def enforce_diversity(self, products: List[CandidateProduct], context: MissionContext) -> List[CandidateProduct]:
        pass
