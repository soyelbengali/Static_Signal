import random

EVENTS = [
    {
        "id": "repeated_voice",
        "title": "REPEATED VOICE",
        "description": "You receive the same call as an hour ago. Same voice. Same words. Same number.",
        "detail": "The log says that call never existed.",
        "effect": "sanity",
        "value": -10,
    },
    {
        "id": "own_number",
        "title": "YOUR OWN NUMBER",
        "description": "A call comes in. The number is yours.",
        "detail": "You don't pick up. The call lasts 47 seconds. There is breathing on the other end.",
        "effect": "sanity",
        "value": -15,
    },
    {
        "id": "lost_unit",
        "title": "UNIT NOT RESPONDING",
        "description": "The dispatched unit confirms arrival at the coordinates. Then, silence.",
        "detail": "The GPS has it pinned at the same spot for 23 minutes. It is not moving.",
        "effect": "sanity",
        "value": -12,
    },
    {
        "id": "own_recording",
        "title": "ANOMALOUS RECORDING",
        "description": "The system plays back a recording from two hours ago. Your voice is in the background.",
        "detail": "You don't remember saying that. You don't remember that moment.",
        "effect": "sanity",
        "value": -18,
    },
    {
        "id": "sudden_clarity",
        "title": "MOMENT OF CLARITY",
        "description": "For a second, everything makes sense. The calls, the coordinates, the pattern.",
        "detail": "Then it's gone. But for a moment you saw it all.",
        "effect": "sanity",
        "value": +20,
    },
    {
        "id": "phone_booth",
        "title": "UNIT REPORT",
        "description": "The unit arrives at coordinates X=-9, Y=-9. It transmits a single message:",
        "detail": '"There is a phone booth here. The receiver is off the hook."',
        "effect": "sanity",
        "value": -20,
    },
    {
        "id": "outgoing_call",
        "title": "UNREGISTERED OUTGOING CALL",
        "description": "The system detects an outgoing call made 4 minutes ago. You didn't make it.",
        "detail": "Or you don't remember.",
        "effect": "sanity",
        "value": -10,
    },
    {
        "id": "clean_signal",
        "title": "CLEAN SIGNAL",
        "description": "For a few minutes, all frequencies are perfectly clean.",
        "detail": "Too clean. As if something had stopped breathing.",
        "effect": "sanity",
        "value": +10,
    },
    {
        "id": "impossible_coordinates",
        "title": "IMPOSSIBLE COORDINATES",
        "description": "A call comes in from coordinates outside the operational range.",
        "detail": "The system logs them. It shouldn't be able to.",
        "effect": "turns",
        "value": -2,
    },
    {
        "id": "fragmented_transmission",
        "title": "FRAGMENTED TRANSMISSION",
        "description": "Through the static, someone says something. You only catch four words:",
        "detail": '"I know you are listening"',
        "effect": "sanity",
        "value": -15,
    },
]


def random_event(probability=0.35):
    if random.random() < probability:
        return random.choice(EVENTS)
    return None


def apply_event(event, operator):
    messages = []
    messages.append(f"\n  ⚠  EVENT — {event['title']}")
    messages.append(f"  {event['description']}")
    messages.append(f"  {event['detail']}")

    if event["effect"] == "sanity":
        operator.sanity += event["value"]
        operator.sanity = min(operator.sanity, operator.sanity_max)
        sign = "+" if event["value"] > 0 else ""
        messages.append(f"  >> Sanity {sign}{event['value']}.")
    elif event["effect"] == "turns":
        operator.turns_remaining += event["value"]
        messages.append(f"  >> Turns remaining {event['value']}.")

    operator.events_log.append(event["title"])
    return messages
