import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_pipeline_status():
    response = client.get("/pipeline/status")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "total_requests" in response.json()
