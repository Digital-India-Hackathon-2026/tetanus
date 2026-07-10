import pytest
from backend.ai.mission.cache import MissionCache
from backend.ai.mission.mission_service import MissionService
from backend.ai.mission.exceptions import MissionNotFoundError

@pytest.fixture(autouse=True)
def reset_cache():
    cache = MissionCache()
    cache.invalidate()
    yield

def test_mission_service_valid():
    service = MissionService()
    ctx = service.resolve({"primary_mission": "Hostel Setup"})
    assert ctx.mission == "Hostel Setup"
    assert ctx.supported is True
    assert len(ctx.primary_categories) > 0
    assert hasattr(ctx, 'metadata')

def test_unsupported_mission():
    service = MissionService()
    with pytest.raises(MissionNotFoundError):
        service.resolve({"primary_mission": "Space Exploration"})

def test_missing_mission():
    service = MissionService()
    with pytest.raises(MissionNotFoundError):
        service.resolve({})

def test_cache_lifecycle():
    cache = MissionCache()
    assert cache._loaded is False
    cache.reload()
    assert cache._loaded is True
    cache.invalidate()
    assert cache._loaded is False

def test_metadata_hash_generation():
    service = MissionService()
    ctx = service.resolve({"primary_mission": "Hostel Setup"})
    assert ctx.metadata.mission_hash is not None
    assert ctx.metadata.load_time_ms > 0
    assert ctx.metadata.source == "AIKB"
