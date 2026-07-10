import pytest
from unittest.mock import MagicMock, patch
from backend.ai.recommendation.retrieval.graph_repository import Neo4jGraphRepository
from backend.ai.recommendation.exceptions import RepositoryError, RetrievalError
from backend.ai.recommendation.models import CandidateProduct

@pytest.fixture
def mock_repo():
    with patch("backend.ai.recommendation.retrieval.graph_repository.GraphDatabase.driver") as mock_driver:
        repo = Neo4jGraphRepository()
        repo.uri = "neo4j://localhost"
        repo.username = "test"
        repo.password = "test"
        yield repo, mock_driver

def test_connect_success(mock_repo):
    repo, mock_driver = mock_repo
    repo.connect()
    assert repo.driver is not None
    mock_driver.assert_called_once()

def test_connect_missing_credentials():
    repo = Neo4jGraphRepository()
    repo.uri = None
    with pytest.raises(RepositoryError):
        repo.connect()

def test_get_product_by_id_success(mock_repo):
    repo, mock_driver = mock_repo
    repo.driver = MagicMock()
    mock_session = MagicMock()
    repo.driver.session.return_value.__enter__.return_value = mock_session
    
    mock_result = MagicMock()
    mock_result.data.return_value = {
        "product_id": "123",
        "name": "Test Product",
        "price": 100.0
    }
    
    mock_session.run.return_value = [mock_result]
    
    product = repo.get_product_by_id("123")
    assert isinstance(product, CandidateProduct)
    assert product.product_id == "123"

def test_get_product_by_id_missing(mock_repo):
    repo, mock_driver = mock_repo
    repo.driver = MagicMock()
    mock_session = MagicMock()
    repo.driver.session.return_value.__enter__.return_value = mock_session
    
    mock_session.run.return_value = []
    
    with pytest.raises(RetrievalError):
        repo.get_product_by_id("999")
