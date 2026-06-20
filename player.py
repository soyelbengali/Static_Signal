class Operator:
    def __init__(self, name, x, y, sanity, turns_max):
        self.name = name
        self.x = x
        self.y = y
        self.sanity = sanity
        self.sanity_max = sanity
        self.turns_remaining = turns_max
        self.turns_completed = 0
        self.events_log = []
        self.sectors_visited = []
        self.end_reason = None
        self.outcome = None
        self._minutes = 23 * 60

    def current_time(self):
        total = self._minutes % (24 * 60)
        return f"{total // 60:02d}:{total % 60:02d}"

    def advance_time(self, minutes=7):
        self._minutes += minutes

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        if not world.in_bounds(new_x, new_y):
            return False, "  >> Out of coverage. You cannot go beyond the operational limits."
        self.x = new_x
        self.y = new_y
        self.turns_remaining -= 1
        self.turns_completed += 1
        return True, None

    def is_alive(self):
        return self.sanity > 0 and self.turns_remaining > 0

    def sanity_status(self):
        ratio = self.sanity / self.sanity_max
        if ratio > 0.75:
            return "STABLE"
        elif ratio > 0.50:
            return "ALERT"
        elif ratio > 0.25:
            return "CRITICAL"
        return "⚠ IMMINENT COLLAPSE"

    def is_hallucinating(self):
        return self.sanity / self.sanity_max < 0.20
