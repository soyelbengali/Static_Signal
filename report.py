import time
import random
from collections import Counter
from map import RED, DARK_RED, BRIGHT_RED, BOLD, YELLOW, GRAY, RESET

SEPARATOR = "─" * 52


def brief_pause():
    time.sleep(0.04)


def print_slow(text, speed=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(speed)
    print()


def show_report(operator, initial_config, signal_detections=0):
    print()
    print(SEPARATOR)
    print("  FINAL REPORT — SHIFT CLOSED")
    print(SEPARATOR)
    time.sleep(0.3)

    print(f"  Operator         : {operator.name}")
    print(f"  Starting position: X={initial_config['x']}, Y={initial_config['y']}")
    print(f"  Starting sanity  : {initial_config['sanity']}")
    print(f"  Max turns        : {initial_config['turns']}")
    print()
    time.sleep(0.2)

    print(f"  Final position   : X={operator.x}, Y={operator.y}")
    print(f"  Turns completed  : {operator.turns_completed}")
    print(f"  Sanity remaining : {max(operator.sanity, 0)}/{operator.sanity_max}")
    print()
    time.sleep(0.2)

    if operator.events_log:
        print("  Logged events:")
        for event in operator.events_log:
            print(f"    — {event}")
    else:
        print("  Logged events: none.")
    print()

    if operator.sectors_visited:
        counts = Counter(sector_type for _, _, sector_type in operator.sectors_visited)
        print("  Sectors visited:")
        for sector_type, n in counts.most_common():
            print(f"    — {sector_type:15} x{n}")
    print()

    print(f"  Signal detections: {signal_detections}")
    print()
    time.sleep(0.2)

    print(f"  Cause of closure : {operator.end_reason}")
    print()
    print(SEPARATOR)
    time.sleep(0.3)

    if operator.outcome == "victory":
        print("  RESULT: SHIFT COMPLETED.")
        print()
        print("  You made it to dawn.")
        print("  The report has been sent.")
        print("  No one has confirmed receiving it.")

    elif operator.outcome in ("collapse", "captured"):
        if operator.outcome == "collapse":
            print("  RESULT: OPERATOR COLLAPSE.")
        else:
            print("  RESULT: SIGNAL LOCATED. OPERATOR ELIMINATED.")
        print()

        system_errors = [
            ("ERROR 174: OPERATIVE DISCONNECTION",              DARK_RED),
            ("ERROR 0x000A12: SIGNAL UNRECOVERABLE",            DARK_RED),
            ("CRITICAL ERROR: RETURN CODE -1",                  RED),
            ("FATAL ERROR: OPERATOR NOT RESPONDING",            BRIGHT_RED),
            ("ERROR 502: SYNCHRONIZATION LOSS",                 DARK_RED),
            ("ERROR 31-B: FREQUENCY CORRUPTED",                 RED),
            ("SYSTEM ERROR: HUMAN INPUT INVALID",               RED),
            ("EXCEPTION RAISED: cognitive_overload()",          RED),
            ("KERNEL FAILURE: audio_stream_lost",               BRIGHT_RED),
            ("ERROR 440: IDENTITY NOT VERIFIED",                DARK_RED),
            ("FATAL SIGNAL LOSS",                               RED),
            ("WARNING: operator out of range",                  YELLOW),
            ("ERROR 7: transmission echo detected",             RED),
            ("STACK OVERFLOW: recursive_channel()",             DARK_RED),
            ("ERROR 991: multiple voices detected",             RED),
            ("RUNTIME ERROR: inconsistent coordinates",         BRIGHT_RED),
            ("ERROR: unexpected call return",                   RED),
            ("BOOTH ERROR: microphone open without operator",   RED),
            ("ERROR 404: operator not found",                   DARK_RED),
            ("ERROR: signal continues after closure",           RED),
        ]

        crash_screen = random.sample(system_errors, random.randint(4, 7))
        for message, color in crash_screen:
            print_slow(f"  {color}{message}{RESET}", random.uniform(0.05, 0.09))
            time.sleep(random.uniform(0.05, 0.2))

        print()
        print_slow("  signal lost", 0.06)
        print_slow("  signal lost", 0.06)
        print_slow("  signal lo",   0.08)
        time.sleep(0.4)
        print()

    elif operator.outcome == "abandoned":
        print("  RESULT: SHIFT ABANDONED.")
        print()
        print("  You left your post.")
        print("  The calls keep coming in.")
        print("  No one picks up.")

    print()
    print(SEPARATOR)
