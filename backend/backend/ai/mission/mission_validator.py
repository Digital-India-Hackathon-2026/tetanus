from backend.ai.mission.exceptions import MissionValidationError

def validate_aikb(mission_knowledge, supported_categories, bundle_knowledge):
    # Process categories
    if isinstance(supported_categories, dict):
        cat_names = set(supported_categories.keys())
    elif isinstance(supported_categories, list):
        cat_names = set(c["category_name"] if isinstance(c, dict) else c for c in supported_categories)
    else:
        cat_names = set()

    # Process bundles
    if isinstance(bundle_knowledge, dict) and "bundles" in bundle_knowledge:
        b_names = set(b.get("bundle_name", b.get("bundle_id", b.get("id", ""))) for b in bundle_knowledge["bundles"])
    elif isinstance(bundle_knowledge, dict):
        b_names = set(bundle_knowledge.keys())
    elif isinstance(bundle_knowledge, list):
        b_names = set(b.get("bundle_name", b.get("bundle_id", b.get("id", ""))) for b in bundle_knowledge)
    else:
        b_names = set()

    # Process missions
    if isinstance(mission_knowledge, dict) and "missions" in mission_knowledge:
        missions = mission_knowledge["missions"]
    else:
        missions = mission_knowledge if isinstance(mission_knowledge, list) else []

    if not missions:
        raise MissionValidationError("Mission knowledge is empty.")

    for m in missions:
        if isinstance(m, str):
            continue
            
        m_name = m.get("mission_name", "Unknown")
        
        # 1. Mission schema is complete
        for field in ["primary_categories", "secondary_categories", "required_categories", "optional_categories", "category_weights", "priority", "mission_type"]:
            if field not in m:
                raise MissionValidationError(f"Mission '{m_name}' is missing required field: {field}")

        req = m.get("required_categories", [])
        opt = m.get("optional_categories", [])
        prim = m.get("primary_categories", [])
        sec = m.get("secondary_categories", [])
        cats = m.get("categories", [])
        weights = m.get("category_weights", {})
        
        # 2. Duplicate categories (req vs opt, prim vs sec)
        if bool(set(req) & set(opt)):
            raise MissionValidationError(f"Mission '{m_name}' has overlapping required and optional categories.")
        if bool(set(prim) & set(sec)):
            raise MissionValidationError(f"Mission '{m_name}' has overlapping primary and secondary categories.")

        # 3. Referenced category exists & 4. Every weighted category exists
        all_cats = list(set(req + opt + prim + sec + cats + list(weights.keys())))
        for c in all_cats:
            if c not in cat_names:
                raise MissionValidationError(f"Mission '{m_name}' references unknown category: '{c}'")

        # 5. Category weights exist, numeric, between 0 and 1
        for c, w in weights.items():
            if not isinstance(w, (int, float)):
                raise MissionValidationError(f"Mission '{m_name}' category '{c}' has non-numeric weight.")
            if not (0 <= w <= 1):
                raise MissionValidationError(f"Mission '{m_name}' category '{c}' has weight outside 0-1 range.")

        # 6. Primary categories have higher weights than secondary categories
        if prim and sec:
            min_prim_weight = min([weights.get(c, 0) for c in prim])
            max_sec_weight = max([weights.get(c, 0) for c in sec])
            if min_prim_weight < max_sec_weight:
                raise MissionValidationError(f"Mission '{m_name}' primary category weight ({min_prim_weight}) is less than a secondary category weight ({max_sec_weight}).")
            
        # 7. Referenced bundle exists
        m_bundles = m.get("bundles", [])
        b_ids = [b.get("bundle_name", b.get("name", "")) if isinstance(b, dict) else b for b in m_bundles]
        # Duplicate bundles within mission
        if len(b_ids) != len(set(b_ids)):
            raise MissionValidationError(f"Mission '{m_name}' has duplicate bundles.")
            
        for b in b_ids:
            if b not in b_names:
                raise MissionValidationError(f"Mission '{m_name}' references unknown bundle: '{b}'")

    return True
