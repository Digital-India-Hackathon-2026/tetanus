from typing import Dict, List, TypedDict

class MissionProfile(TypedDict):
    essential: List[str]
    optional: List[str]

MISSION_PROFILES: Dict[str, MissionProfile] = {
    "hostel setup": {
        "essential": ["mattress", "bucket", "mug", "bedsheet", "pillow", "lamp"],
        "optional": ["extension board", "laundry basket", "storage box"]
    },
    "work from home": {
        "essential": ["laptop stand", "keyboard", "mouse", "chair", "desk lamp"],
        "optional": ["monitor", "mousepad", "headphones"]
    },
    "travel": {
        "essential": ["power bank", "neck pillow", "travel adapter", "toiletry kit"],
        "optional": ["luggage tag", "packing cubes", "eye mask"]
    },
    "gym": {
        "essential": ["protein shaker", "gym gloves", "water bottle", "resistance bands"],
        "optional": ["gym bag", "towel", "fitness tracker"]
    },
    "movie night": {
        "essential": ["blanket", "popcorn", "snacks", "speaker"],
        "optional": ["projector", "cushions", "led lights"]
    },
    "birthday party": {
        "essential": ["decorations", "candles", "cake knife", "disposable plates"],
        "optional": ["balloons", "party hats", "return gifts"]
    },
    "gaming setup": {
        "essential": ["gaming mouse", "mechanical keyboard", "headset", "mousepad"],
        "optional": ["rgb strip", "controller", "monitor arm"]
    },
    "college essentials": {
        "essential": ["backpack", "notebooks", "pens", "water bottle", "laptop sleeve"],
        "optional": ["highlighters", "calculator", "sticky notes"]
    }
}

def get_mission_profile(mission_name: str) -> MissionProfile:
    """Returns the mission profile (essentials/optionals) for a given mission name, or empty lists if not found."""
    return MISSION_PROFILES.get(mission_name.lower(), {"essential": [], "optional": []})
