import pytest
import time
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def slow_down_tests():
    yield
    print("Sleeping 10s to avoid rate limit...")
    time.sleep(10)


def test_adversarial_empty_query():
    response = client.post("/api/v1/recommend", json={"query": ""})
    # Might return 422 or unsupported, but should NOT crash (500)
    assert response.status_code in [200, 422]

def test_adversarial_sql_injection():
    response = client.post("/api/v1/recommend", json={"query": "DROP TABLE products; --"})
    assert response.status_code == 200
    # Should probably hit unsupported mission or just return no results
    assert response.json().get("status") in ["success", "needs_clarification"]

def test_adversarial_huge_string():
    response = client.post("/api/v1/recommend", json={"query": "A" * 10000})
    # Should handle gracefully, either 413, 422, or 200
    assert response.status_code != 500

def test_adversarial_emojis():
    response = client.post("/api/v1/recommend", json={"query": "I want a 💻 for my 🏠"})
    assert response.status_code == 200

def test_unsupported_mission():
    response = client.post("/api/v1/recommend", json={"query": "I want to buy a flight ticket to London"})
    assert response.status_code == 200
    data = response.json()
    assert data["products"] == []
    assert data["bundles"] == []
    assert data.get("status") in ["unsupported", "needs_clarification"]
