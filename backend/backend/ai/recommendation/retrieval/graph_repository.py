import os
import time
from typing import List, Dict, Any
from neo4j import GraphDatabase, exceptions as neo4j_exceptions

from backend.ai.recommendation.retrieval.repository import GraphRepositoryInterface
from backend.ai.recommendation.models import CandidateProduct
from backend.ai.recommendation.exceptions import RetrievalError, RepositoryError
from backend.ai.recommendation.retrieval.graph_queries import (
    GET_PRODUCT_BY_ID,
    GET_PRODUCTS_BY_CATEGORY,
    GET_PRODUCTS_BY_BRAND,
    GET_PRODUCTS,
    SEARCH_PRODUCTS,
    GET_PRODUCT_CONTEXT
)

class Neo4jGraphRepository(GraphRepositoryInterface):
    def __init__(self):
        self.uri = os.environ.get("NEO4J_URI")
        self.username = os.environ.get("NEO4J_USERNAME")
        self.password = os.environ.get("NEO4J_PASSWORD")
        self.database = os.environ.get("NEO4J_DATABASE", "neo4j")
        self.driver = None

    def connect(self):
        if not self.uri or not self.username or not self.password:
            raise RepositoryError("Missing Neo4j credentials in environment variables.")
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
            self.driver.verify_connectivity()
        except neo4j_exceptions.AuthError as e:
            raise RepositoryError(f"Neo4j Authentication failed: {e}")
        except Exception as e:
            raise RepositoryError(f"Failed to connect to Neo4j: {e}")

    def close(self):
        if self.driver:
            self.driver.close()

    def health_check(self) -> Dict[str, Any]:
        start_time = time.time()
        status = {
            "connected": False,
            "database": self.database,
            "latency_ms": 0.0,
            "node_counts": {
                "products": 0,
                "categories": 0,
                "brands": 0
            }
        }
        
        try:
            if not self.driver:
                self.connect()
                
            with self.driver.session(database=self.database) as session:
                product_count = session.run("MATCH (n:Product) RETURN count(n) AS c").single()["c"]
                category_count = session.run("MATCH (n:Category) RETURN count(n) AS c").single()["c"]
                brand_count = session.run("MATCH (n:Brand) RETURN count(n) AS c").single()["c"]
                
                status["node_counts"]["products"] = product_count
                status["node_counts"]["categories"] = category_count
                status["node_counts"]["brands"] = brand_count
                status["connected"] = True
                
        except Exception as e:
            status["connected"] = False
            status["error"] = str(e)
            
        status["latency_ms"] = (time.time() - start_time) * 1000
        return status

    def execute_query(self, query: str, params: Dict[str, Any] = None) -> Any:
        if not self.driver:
            self.connect()
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, params or {})
                return [record.data() for record in result]
        except Exception as e:
            raise RepositoryError(f"Neo4j Query Execution failed: {e}")

    def _map_to_candidate_product(self, record: dict) -> CandidateProduct:
        try:
            return CandidateProduct(
                product_id=record["product_id"],
                name=record["name"],
                brand=record.get("brand"),
                category=record.get("category"),
                price=float(record["price"]) if record.get("price") is not None else 0.0,
                mrp=float(record["mrp"]) if record.get("mrp") is not None else None,
                rating=float(record["rating"]) if record.get("rating") is not None else None,
                review_count=int(record["review_count"]) if record.get("review_count") is not None else None,
                description=record.get("description"),
                image_url=record.get("image_url"),
                product_url=record.get("product_url"),
                quality_score=float(record["quality_score"]) if record.get("quality_score") is not None else None
            )
        except KeyError as e:
            raise RetrievalError(f"Missing required property in Neo4j result: {e}")
        except Exception as e:
            raise RetrievalError(f"Failed to map Neo4j record to CandidateProduct: {e}")

    def get_product_by_id(self, product_id: str) -> CandidateProduct:
        records = self.execute_query(GET_PRODUCT_BY_ID, {"product_id": product_id})
        if not records:
            raise RetrievalError(f"Product not found: {product_id}")
        return self._map_to_candidate_product(records[0])

    def get_products_by_categories(self, categories: List[str], limit: int = 100) -> List[CandidateProduct]:
        if not categories:
            return []
        records = self.execute_query(GET_PRODUCTS_BY_CATEGORY, {"categories": categories, "limit": limit})
        return [self._map_to_candidate_product(r) for r in records]

    def get_products_by_brands(self, brands: List[str], limit: int = 100) -> List[CandidateProduct]:
        if not brands:
            return []
        records = self.execute_query(GET_PRODUCTS_BY_BRAND, {"brands": brands, "limit": limit})
        return [self._map_to_candidate_product(r) for r in records]

    def get_products(self, categories: List[str] = None, brands: List[str] = None) -> List[CandidateProduct]:
        records = self.execute_query(GET_PRODUCTS, {"categories": categories or [], "brands": brands or []})
        return [self._map_to_candidate_product(r) for r in records]

    def search_products(self, keyword: str) -> List[CandidateProduct]:
        if not keyword:
            return []
        records = self.execute_query(SEARCH_PRODUCTS, {"keyword": keyword})
        return [self._map_to_candidate_product(r) for r in records]

    def get_product_context(self, product_id: str) -> CandidateProduct:
        records = self.execute_query(GET_PRODUCT_CONTEXT, {"product_id": product_id})
        if not records:
            raise RetrievalError(f"Product not found: {product_id}")
        return self._map_to_candidate_product(records[0])

    # TODO: Future Graph Extensions
    def get_similar_products(self, product_id: str) -> List[CandidateProduct]:
        return []

    def get_bundle_products(self, bundle_id: str) -> List[CandidateProduct]:
        return []
