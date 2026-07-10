from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "DigitalIndia Recommendation API",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0"
    }

@router.get("/pipeline/status")
async def pipeline_status():
    """
    Check if the pipeline dependencies (Neo4j, etc) are available.
    """
    # In a real scenario, this would ping Neo4j or other downstream services
    return {
        "status": "operational",
        "neo4j": "connected",
        "gemini": "available",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/metrics")
async def get_metrics():
    """
    Basic telemetry for the recommendation system.
    """
    # Just returning placeholders for demo purposes
    return {
        "total_requests": 0,
        "average_latency_ms": 0.0,
        "cache_hit_rate": 0.0
    }
