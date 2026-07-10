from typing import List, Dict, Any
from abc import ABC, abstractmethod
from backend.ai.recommendation.models import CandidateProduct

class GraphRepositoryInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> Any:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: str) -> CandidateProduct:
        pass

    @abstractmethod
    def get_products_by_categories(self, categories: List[str]) -> List[CandidateProduct]:
        pass

    @abstractmethod
    def get_products_by_brands(self, brands: List[str]) -> List[CandidateProduct]:
        pass

    @abstractmethod
    def get_products(self, categories: List[str] = None, brands: List[str] = None) -> List[CandidateProduct]:
        pass

    @abstractmethod
    def search_products(self, keyword: str) -> List[CandidateProduct]:
        pass

    @abstractmethod
    def get_product_context(self, product_id: str) -> CandidateProduct:
        pass

    # TODO: Future Graph Extensions
    @abstractmethod
    def get_similar_products(self, product_id: str) -> List[CandidateProduct]:
        pass

    @abstractmethod
    def get_bundle_products(self, bundle_id: str) -> List[CandidateProduct]:
        pass

class PostgresRepositoryInterface(ABC):
    @abstractmethod
    def get_prices(self, product_ids: List[str]) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_inventory(self, product_ids: List[str]) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_ratings(self, product_ids: List[str]) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_reviews(self, product_ids: List[str]) -> Dict[str, int]:
        pass
