from backend.ai.mission.cache import MissionCache

class MissionLoader:
    def __init__(self):
        self.cache = MissionCache()
        
    def load_mission(self, mission_name: str):
        return self.cache.get_mission(mission_name)
        
    def load_bundles(self):
        return self.cache.get_bundle_knowledge()
        
    def load_supported_categories(self):
        return self.cache.get_supported_categories()
        
    def get_metadata(self):
        return self.cache.get_metadata()
        
    def get_load_time_ms(self):
        return self.cache.get_load_time_ms()
