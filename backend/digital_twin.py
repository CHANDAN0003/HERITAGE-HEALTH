class BuildingTwin:
    def __init__(self):
        self.pillars = {
            "P1": {"health": 100},
            "P2": {"health": 100},
            "P3": {"health": 100},
            "P4": {"health": 100}
        }
        self.overall_health = 100

    def update_pillar(self, name, anomaly_score):
        damage = abs(anomaly_score) * 12
        self.pillars[name]["health"] = max(
            0, self.pillars[name]["health"] - int(damage)
        )

    def update_building_health(self):
        total = sum(p["health"] for p in self.pillars.values())
        self.overall_health = int(total / 4)

    def get_state(self):
        return {
            "overall_health": self.overall_health,
            "pillars": self.pillars
        }
