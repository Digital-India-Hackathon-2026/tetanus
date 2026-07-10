import pathlib

def fix_file(path, replace_pairs):
    txt = pathlib.Path(path).read_text(encoding="utf-8")
    for old, new in replace_pairs:
        txt = txt.replace(old, new)
    pathlib.Path(path).write_text(txt, encoding="utf-8")

# For test_diversity.py
fix_file("backend/ai/recommendation/tests/test_diversity.py", [
    ('import pytest', 'import pytest\nfrom backend.ai.mission.mission_models import MissionMetadata\n\ndef get_mission_ctx(bundle_ids=None):\n    meta = MissionMetadata(aikb_version="1.0", schema_version="1.0", generated_at="2026", mission_hash="abc", source="test", loaded_from="test", load_time_ms=1.0)\n    return MissionContext(mission="test", intent_type="test", supported=True, definition={}, primary_categories=[], secondary_categories=[], required_categories=[], optional_categories=[], category_weights={}, bundle_ids=bundle_ids or [], priority="P1", mission_type="test", metadata=meta)'),
    ('MissionContext(mission="test", intent_type="test")', 'get_mission_ctx()')
])

# For test_bundling.py
fix_file("backend/ai/recommendation/tests/test_bundling.py", [
    ('import pytest', 'import pytest\nfrom backend.ai.mission.mission_models import MissionMetadata\n\ndef get_mission_ctx(bundle_ids=None):\n    meta = MissionMetadata(aikb_version="1.0", schema_version="1.0", generated_at="2026", mission_hash="abc", source="test", loaded_from="test", load_time_ms=1.0)\n    return MissionContext(mission="test", intent_type="test", supported=True, definition={}, primary_categories=[], secondary_categories=[], required_categories=[], optional_categories=[], category_weights={}, bundle_ids=bundle_ids or [], priority="P1", mission_type="test", metadata=meta)'),
    ('MissionContext(mission="test", intent_type="test", bundle_ids=["Test Bundle 1"])', 'get_mission_ctx(bundle_ids=["Test Bundle 1"])'),
    ('MissionContext(mission="test", intent_type="test", bundle_ids=["Test Bundle 2"])', 'get_mission_ctx(bundle_ids=["Test Bundle 2"])')
])
