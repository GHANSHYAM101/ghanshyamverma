# stats_manager.py
from threading import Lock

class StatsManager:
    def __init__(self):
        self.total_vehicles = 0
        self.total_violations = 0
        self.lock = Lock()

    def increment_vehicle(self):
        with self.lock:
            self.total_vehicles += 1

    def increment_violation(self):
        with self.lock:
            self.total_violations += 1

    def get_stats(self):
        with self.lock:
            return {
                "vehicles":   self.total_vehicles,
                "violations": self.total_violations
            }

# a single shared instance
stats = StatsManager()
