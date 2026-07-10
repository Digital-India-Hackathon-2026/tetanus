import time

class TelemetryTracker:
    def __init__(self):
        self.retrieved_products = 0
        self.filtered_products = 0
        self.returned_products = 0
        self.execution_time_ms = 0.0
        self.ranking_time_ms = 0.0
        self.filter_time_ms = 0.0
        self.bundle_time_ms = 0.0
        self.repository_time_ms = 0.0
        
        self._timers = {}

    def start_timer(self, name: str):
        self._timers[name] = time.time()

    def stop_timer(self, name: str, attr: str):
        if name in self._timers:
            elapsed = (time.time() - self._timers.pop(name)) * 1000
            setattr(self, attr, getattr(self, attr, 0.0) + elapsed)

    def record_counts(self, retrieved=0, filtered=0, returned=0):
        self.retrieved_products += retrieved
        self.filtered_products += filtered
        self.returned_products += returned
