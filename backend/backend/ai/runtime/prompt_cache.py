import time
from typing import Tuple, Any

class MemoryCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self.cache = {}

    def get(self, key: str, check_mtime: float = None) -> Tuple[Any, bool]:
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] <= self.ttl_seconds:
                if check_mtime is None or entry.get('mtime') == check_mtime:
                    return entry['data'], True
        return None, False

    def set(self, key: str, data: Any, mtime: float = None):
        self.cache[key] = {
            'data': data,
            'timestamp': time.time(),
            'mtime': mtime
        }
