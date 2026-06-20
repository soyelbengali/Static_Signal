import random

MAP_MIN = -10
MAP_MAX = 10

NOISY_SECTORS = {"call", "interference"}
DETECTION_RANGE = 4
PURSUIT_TURNS_MIN = 4
PURSUIT_TURNS_MAX = 12

SECTOR_TYPES = {
    "empty":        {"description": "No activity recorded in this sector.",              "effect": None},
    "call":         {"description": "Active call signal.",                               "effect": "call"},
    "silence":      {"description": "Zone of total silence. No signal.",                 "effect": "silence"},
    "interference": {"description": "Severe interference. Data is corrupted.",           "effect": "interference"},
    "shelter":      {"description": "Repeater station. Stable signal.",                  "effect": "shelter"},
    "anomaly":      {"description": "Coordinate that appears on no official map.",       "effect": "anomaly"},
    "coffee":       {"description": "Coffee machine. Still working.",                    "effect": "coffee"},
    "log":          {"description": "Someone left a shift log here.",                    "effect": "log"},
    "old_radio":    {"description": "An old radio playing static music.",                "effect": "old_radio"},
    "photo":        {"description": "A family photo. You don't remember who they are.",  "effect": "photo"},
}

SECTOR_WEIGHTS = [
    ("empty",        30),
    ("call",         18),
    ("silence",       8),
    ("interference", 13),
    ("shelter",       8),
    ("anomaly",       5),
    ("coffee",        7),
    ("log",           5),
    ("old_radio",     4),
    ("photo",         2),
]

SECTOR_USES = {
    "shelter":   3,
    "coffee":    2,
    "log":       1,
    "old_radio": 2,
    "photo":     1,
}

BROKEN_TEXTS = {
    "empty": [
        "  >> the sector is e m p t y",
        "  >> nothing. nothing. nothing. nothing.",
        "  >> no activity. that's what the system says.",
    ],
    "call": [
        "  >> the voice says your name",
        "  >> you can't hang up. you know you can't hang up.",
        "  >> the call has been open for too long",
    ],
    "silence": [
        "  >> too much silence. something is absorbing it.",
        "  >> no signal. nothing. you are alone.",
        "  >> the silence has a shape",
    ],
    "interference": [
        "  >> the data says this is not happening",
        "  >> ERROR ERROR ERROR",
        "  >> someone is recording this",
    ],
    "shelter": [
        "  >> the signal is clean. you are not.",
        "  >> it works. for now.",
        "  >> you breathe. or something that resembles breathing.",
    ],
    "coffee": [
        "  >> the coffee tastes like something that isn't coffee",
        "  >> you drink it anyway",
    ],
    "log": [
        "  >> the handwriting is yours. you don't remember writing it.",
        "  >> the last page is blank. or almost.",
    ],
    "old_radio": [
        "  >> the song ends. it starts again from the beginning.",
        "  >> someone is singing on a frequency that shouldn't exist.",
    ],
    "photo": [
        "  >> the person in the photo is looking at you.",
        "  >> there is someone behind them. you hadn't noticed before.",
    ],
}


def random_sector_type():
    types = [t for t, _ in SECTOR_WEIGHTS]
    weights = [w for _, w in SECTOR_WEIGHTS]
    return random.choices(types, weights=weights, k=1)[0]


def manhattan_distance(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)


def broken_sector_text(sector_type):
    options = BROKEN_TEXTS.get(sector_type, ["  >> ."])
    return random.choice(options)


class Sector:
    def __init__(self, x, y, sector_type=None):
        self.x = x
        self.y = y
        self.type = sector_type if sector_type else random_sector_type()
        self.visited = False
        self.uses = 0

    def description(self):
        return SECTOR_TYPES[self._active_type()]["description"]

    def effect(self):
        return SECTOR_TYPES[self._active_type()]["effect"]

    def _active_type(self):
        max_uses = SECTOR_USES.get(self.type)
        if max_uses is not None and self.uses >= max_uses:
            return "empty"
        return self.type

    def visible_type(self):
        return self._active_type()


class Signal:
    def __init__(self):
        self.x = random.randint(MAP_MIN, MAP_MAX)
        self.y = random.randint(MAP_MIN, MAP_MAX)
        self.phase = "patrol"
        self.pursuit_turns = 0
        self.pursuit_turn_limit = 0
        self.retreat_turns = 0
        self.times_detected = 0

    def check_detection(self, operator, sector_type):
        if self.phase == "retreat":
            return False, ""
        dist = manhattan_distance(self.x, self.y, operator.x, operator.y)
        if dist <= DETECTION_RANGE:
            return True, f"critical distance ({dist} steps)"
        if sector_type in NOISY_SECTORS:
            trigger_chance = 0.55 if sector_type == "interference" else 0.35
            if random.random() < trigger_chance:
                return True, f"sector noise [{sector_type.upper()}]"
        return False, ""

    def start_pursuit(self):
        self.phase = "pursuit"
        self.pursuit_turns = 0
        self.pursuit_turn_limit = random.randint(PURSUIT_TURNS_MIN, PURSUIT_TURNS_MAX)
        self.times_detected += 1

    def _start_retreat(self):
        self.phase = "retreat"
        self.retreat_turns = 0

    def _return_to_patrol(self):
        self.phase = "patrol"
        edge = random.choice(["N", "S", "E", "W"])
        if edge == "N":
            self.x = random.randint(MAP_MIN, MAP_MAX)
            self.y = MAP_MAX
        elif edge == "S":
            self.x = random.randint(MAP_MIN, MAP_MAX)
            self.y = MAP_MIN
        elif edge == "E":
            self.x = MAP_MAX
            self.y = random.randint(MAP_MIN, MAP_MAX)
        else:
            self.x = MAP_MIN
            self.y = random.randint(MAP_MIN, MAP_MAX)

    def _move_patrol(self):
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.x = max(MAP_MIN, min(MAP_MAX, self.x + dx))
        self.y = max(MAP_MIN, min(MAP_MAX, self.y + dy))

    def _move_pursuit(self, target_x, target_y):
        if self.x < target_x:   self.x += 1
        elif self.x > target_x: self.x -= 1
        if self.y < target_y:   self.y += 1
        elif self.y > target_y: self.y -= 1
        self.pursuit_turns += 1
        if self.pursuit_turns >= self.pursuit_turn_limit:
            self._start_retreat()

    def _move_retreat(self):
        dx = -1 if self.x <= 0 else 1
        dy = -1 if self.y <= 0 else 1
        self.x += dx
        self.y += dy
        self.retreat_turns += 1
        if self.x < MAP_MIN or self.x > MAP_MAX or self.y < MAP_MIN or self.y > MAP_MAX:
            self._return_to_patrol()

    def move(self, target_x, target_y):
        if self.phase == "patrol":
            self._move_patrol()
        elif self.phase == "pursuit":
            self._move_pursuit(target_x, target_y)
        elif self.phase == "retreat":
            self._move_retreat()

    def collision(self, op_x, op_y):
        return self.phase == "pursuit" and self.x == op_x and self.y == op_y

    def distance_to(self, op_x, op_y):
        return manhattan_distance(self.x, self.y, op_x, op_y)


class World:
    def __init__(self):
        self.sectors = {}
        self.signal = Signal()

    def get_sector(self, x, y):
        if (x, y) not in self.sectors:
            self.sectors[(x, y)] = Sector(x, y)
        return self.sectors[(x, y)]

    def in_bounds(self, x, y):
        return MAP_MIN <= x <= MAP_MAX and MAP_MIN <= y <= MAP_MAX

    def apply_effect(self, sector, operator):
        effect = sector.effect()
        messages = []

        if sector.type in SECTOR_USES:
            sector.uses += 1
            uses_left = SECTOR_USES[sector.type] - sector.uses
            if uses_left == 0:
                messages.append("  >> This sector is depleted. It won't work again.")
            elif uses_left == 1:
                messages.append("  >> Only one use left in this sector.")

        if effect == "call":
            messages += self._effect_call(operator)
        elif effect == "silence":
            messages += self._effect_silence(operator)
        elif effect == "interference":
            messages += self._effect_interference(operator)
        elif effect == "shelter":
            messages += self._effect_shelter(operator)
        elif effect == "anomaly":
            messages += self._effect_anomaly(operator)
        elif effect == "coffee":
            messages += self._effect_coffee(operator)
        elif effect == "log":
            messages += self._effect_log(operator)
        elif effect == "old_radio":
            messages += self._effect_old_radio(operator)
        elif effect == "photo":
            messages += self._effect_photo(operator)

        return messages

    def _drain_sanity(self, operator, amount):
        operator.sanity -= amount
        return f"  >> Sanity -{amount}."

    def _restore_sanity(self, operator, amount):
        operator.sanity += amount
        operator.sanity = min(operator.sanity, operator.sanity_max)
        return f"  >> Sanity +{amount}."

    def _effect_call(self, operator):
        loss = random.randint(5, 15)
        return [
            "  >> Incoming call. Unrecognizable voice.",
            self._drain_sanity(operator, loss),
        ]

    def _effect_silence(self, operator):
        loss = random.randint(1, 8)
        return [
            "  >> Total silence. No static. Nothing.",
            self._drain_sanity(operator, loss),
        ]

    def _effect_interference(self, operator):
        loss = random.randint(10, 20)
        return [
            "  >> SEVERE INTERFERENCE. Records corrupted.",
            self._drain_sanity(operator, loss),
        ]

    def _effect_shelter(self, operator):
        gain = random.randint(8, 20)
        return [
            "  >> Repeater station active. Clean signal.",
            self._restore_sanity(operator, gain),
        ]

    def _effect_anomaly(self, operator):
        loss = random.randint(15, 25)
        new_x = random.randint(MAP_MIN, MAP_MAX)
        new_y = random.randint(MAP_MIN, MAP_MAX)
        operator.x = new_x
        operator.y = new_y
        operator.sanity -= loss
        return [
            "  >> ANOMALOUS COORDINATE.",
            f"  >> The signal pulls you. Relocated to X={new_x}, Y={new_y}.",
            f"  >> Sanity -{loss}.",
        ]

    def _effect_coffee(self, operator):
        gain = random.randint(5, 12)
        operator.sanity += gain
        operator.sanity = min(operator.sanity, operator.sanity_max)
        return [
            "  >> Cold coffee. But coffee.",
            f"  >> Sanity +{gain}. You clear your head a little.",
        ]

    def _effect_log(self, operator):
        gain = random.randint(8, 15)
        entries = [
            "Someone wrote: 'if you read this, they already know you are here'.",
            "Last entry: '03:41 — do not answer line 4'.",
            "Tight handwriting: 'the negative coordinates are not real. repeat: not real'.",
            "Smudged ink: 'I found the pattern. It doesn't help'.",
        ]
        operator.sanity += gain
        operator.sanity = min(operator.sanity, operator.sanity_max)
        return [
            f"  >> {random.choice(entries)}",
            f"  >> Sanity +{gain}. Knowing you're not the first helps.",
        ]

    def _effect_old_radio(self, operator):
        gain = random.randint(6, 14)
        broadcasts = [
            "Something that sounds like jazz. You can't place the song.",
            "A voice reading the weather from three days ago.",
            "Music. Stops. Music. As if someone were changing the dial.",
            "Just static, but rhythmic. Almost comforting.",
        ]
        operator.sanity += gain
        operator.sanity = min(operator.sanity, operator.sanity_max)
        return [
            f"  >> {random.choice(broadcasts)}",
            f"  >> Sanity +{gain}.",
        ]

    def _effect_photo(self, operator):
        gain = random.randint(10, 18)
        details = [
            "Two people on a beach. Happy. The back says 'August'.",
            "A child with a dog. The photo is burned on one side.",
            "Someone standing in front of this very building. Daytime. It looks like another place.",
        ]
        operator.sanity += gain
        operator.sanity = min(operator.sanity, operator.sanity_max)
        return [
            f"  >> {random.choice(details)}",
            f"  >> Sanity +{gain}. It reminds you there was a before.",
        ]
