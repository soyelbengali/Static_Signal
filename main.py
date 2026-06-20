import random
import time
import sys

from world import World, MAP_MIN, MAP_MAX, broken_sector_text
from player import Operator
from events import random_event, apply_event
from report import show_report, SEPARATOR
from map import draw_map, RED, BOLD, YELLOW, GRAY, RESET
import sound

DIRECTIONS = {
    "n":  ( 0,  1), "s":  ( 0, -1),
    "e":  ( 1,  0), "w":  (-1,  0),
    "ne": ( 1,  1), "nw": (-1,  1),
    "se": ( 1, -1), "sw": (-1, -1),
}

DIRECTION_ALIASES = {
    "north": "n", "up":    "n",
    "south": "s", "down":  "s",
    "east":  "e", "right": "e",
    "west":  "w", "left":  "w",
}

DIFFICULTY_LEVELS = {
    "1": {"name": "easy",   "sanity": 100, "turns": 20, "event_chance": 0.20},
    "2": {"name": "normal", "sanity":  80, "turns": 30, "event_chance": 0.35},
    "3": {"name": "hard",   "sanity":  60, "turns": 40, "event_chance": 0.50},
}

EVENT_SOUNDS = {
    "repeated_voice":           sound.sound_repeated_voice,
    "own_number":               sound.sound_own_number,
    "lost_unit":                sound.sound_lost_unit,
    "own_recording":            sound.sound_recording,
    "sudden_clarity":           sound.sound_moment_of_clarity,
    "phone_booth":              sound.sound_lost_unit,
    "outgoing_call":            sound.sound_repeated_voice,
    "clean_signal":             sound.sound_clean_signal,
    "impossible_coordinates":   sound.sound_impossible_coordinates,
    "fragmented_transmission":  sound.sound_fragmented_transmission,
}


def pause(seconds=0.3):
    time.sleep(seconds)


def prompt_name(question, default="Operator"):
    entry = input(question).strip()
    return entry if entry else default


def show_intro():
    print()
    print(SEPARATOR)
    print()
    pause(0.2)
    print("  STATIC SIGNAL")
    pause(0.1)
    frequency = round(random.uniform(150.0, 160.0), 1)
    print(f"  Night shift. Frequency {frequency} MHz.")
    pause(0.1)
    print("  You are the only one listening.")
    print()
    pause(0.3)
    print(SEPARATOR)
    pause(0.4)
    print()
    print("  You have been working the night shift for three years.")
    print("  You know the difference between a drunk and a real emergency.")
    print("  You know when someone is really crying.")
    print()
    print("  Tonight something is different.")
    print()
    pause(0.5)
    print(SEPARATOR)
    print()


def configure_shift():
    print("  SHIFT CONFIGURATION")
    print()
    operator_name = prompt_name("  Operator name (Enter = 'Operator'): ")
    print()
    print("  Difficulty:")
    for key, level in DIFFICULTY_LEVELS.items():
        print(f"    {key}. {level['name']:8} — sanity {level['sanity']}, turns {level['turns']}")
    choice = input("  Choose (1/2/3, Enter = 2): ").strip()
    if choice not in DIFFICULTY_LEVELS:
        choice = "2"
    chosen_level = DIFFICULTY_LEVELS[choice]
    print()
    print(SEPARATOR)
    print()
    print(f"  Operator         : {operator_name}")
    print(f"  Starting position: X=0, Y=0")
    print(f"  Sanity           : {chosen_level['sanity']}")
    print(f"  Target turns     : {chosen_level['turns']}")
    print(f"  Difficulty       : {chosen_level['name']}")
    print()
    print(f"  Operational area : X=[{MAP_MIN},{MAP_MAX}]  Y=[{MAP_MIN},{MAP_MAX}]")
    print("  Victory  : survive all turns")
    print("  Defeat   : sanity=0 / captured / abandon")
    print()
    print(SEPARATOR)
    print()
    return operator_name, chosen_level


def show_turn_header(operator, world, turn_number, total_turns):
    print(f"\n  — TURN {turn_number}/{total_turns}   {operator.current_time()} —")
    draw_map(operator, world)
    print(f"  Mental state     : [{operator.sanity_status()}]")
    print(f"  Turns remaining  : {operator.turns_remaining}")


def prompt_direction():
    print()
    print("  Directions: n / s / e / w / ne / nw / se / sw")
    print("  (type 'quit' to abandon the shift)")
    while True:
        entry = input("  > ").strip().lower()
        if entry == "quit":
            return None
        entry = DIRECTION_ALIASES.get(entry, entry)
        if entry in DIRECTIONS:
            return entry
        print("  Direction not recognized.")


def handle_sector_entry(operator, sector):
    if sector.visited:
        return
    sector.visited = True
    operator.sectors_visited.append((operator.x, operator.y, sector.visible_type()))
    sound.sound_sector(sector.type)


def print_sector_description(operator, sector):
    sector_type = sector.visible_type()
    print(f"  Sector  : {sector_type.upper()} — {sector.description()}")
    if operator.is_hallucinating():
        print(broken_sector_text(sector_type))


def apply_sector_effects(operator, world, sector):
    effects = world.apply_effect(sector, operator)
    for line in effects:
        print(line)
        pause(0.04)


def handle_signal_detection(signal, operator, sector):
    previous_phase = signal.phase
    detected, reason = signal.check_detection(operator, sector.type)
    if detected and signal.phase == "patrol":
        signal.start_pursuit()
        sound.sound_detection()
        print(f"\n  {RED}{BOLD}⚠  SIGNAL DETECTED — {reason.upper()}{RESET}")
        print(f"  {RED}Something is coming for you.{RESET}")
        pause(0.2)
    signal.move(operator.x, operator.y)
    if signal.phase != previous_phase:
        _print_phase_change(signal.phase)


def _print_phase_change(new_phase):
    if new_phase == "retreat":
        print(f"\n  {YELLOW}  The signal loses your trail. It retreats.{RESET}")
        sound.resume_static()
    elif new_phase == "patrol":
        print(f"\n  {GRAY}  Silence. The signal goes back to wandering.{RESET}")


def handle_signal_collision(operator, signal):
    if not signal.collision(operator.x, operator.y):
        return False
    sound.pause_static()
    sound.sound_death()
    print()
    print(f"  {RED}{BOLD}THE SIGNAL HAS FOUND YOU.{RESET}")
    print()
    operator.outcome = "captured"
    operator.end_reason = "Captured by hostile entity"
    return True


def handle_random_event(operator, event_chance):
    event = random_event(event_chance)
    if not event:
        return
    sound_fn = EVENT_SOUNDS.get(event["id"])
    if sound_fn:
        sound_fn()
    event_messages = apply_event(event, operator)
    for line in event_messages:
        print(line)
        pause(0.04)


def handle_movement(operator, world):
    direction = prompt_direction()
    if direction is None:
        operator.outcome = "abandoned"
        operator.end_reason = "Operator abandoned the shift"
        return

    dx, dy = DIRECTIONS[direction]
    previous_pos = (operator.x, operator.y)
    moved, error_message = operator.move(dx, dy, world)

    if not moved:
        print(f"\n{error_message}")
        operator.turns_remaining -= 1
        operator.turns_completed += 1
    else:
        print(f"\n  Move: {direction.upper()}"
              f"  |  ({previous_pos[0]},{previous_pos[1]}) → ({operator.x},{operator.y})")

    pause(0.1)


def resolve_end_state(operator):
    if operator.sanity <= 0:
        operator.end_reason = "Sanity depleted — operator collapse"
        operator.outcome = "collapse"
        sound.pause_static()
        sound.sound_death()
    else:
        operator.end_reason = "Operational time exhausted"
        operator.outcome = "abandoned"


def run_shift(operator, world, level):
    total_turns = level["turns"]
    event_chance = level["event_chance"]
    initial_config = {
        "x": operator.x, "y": operator.y,
        "sanity": operator.sanity_max,
        "turns": operator.turns_remaining,
    }

    turn_number = 0

    while operator.is_alive():
        turn_number += 1

        if turn_number > total_turns:
            operator.outcome = "victory"
            operator.end_reason = "Survival completed"
            sound.sound_victory()
            break

        show_turn_header(operator, world, turn_number, total_turns)
        operator.advance_time(7)

        sector = world.get_sector(operator.x, operator.y)
        handle_sector_entry(operator, sector)
        print_sector_description(operator, sector)
        apply_sector_effects(operator, world, sector)

        if not operator.is_alive():
            break

        signal = world.signal
        handle_signal_detection(signal, operator, sector)

        if handle_signal_collision(operator, signal):
            break

        handle_random_event(operator, event_chance)

        if not operator.is_alive():
            break

        handle_movement(operator, world)

        if operator.outcome is not None:
            break

    if operator.outcome is None:
        resolve_end_state(operator)

    show_report(operator, initial_config, world.signal.times_detected)
    sound.pause_static()


def play():
    show_intro()
    sound.start_static()
    operator_name, level = configure_shift()

    world = World()
    operator = Operator(
        name=operator_name, x=0, y=0,
        sanity=level["sanity"],
        turns_max=level["turns"],
    )

    print("  Starting shift...")
    pause(0.8)
    print()
    run_shift(operator, world, level)


def main():
    while True:
        play()
        print()
        answer = input("  Start a new shift? (y/n): ").strip().lower()
        if answer not in ("y", "yes", "s", "si", "sí"):
            print()
            print("  Closing session.")
            print()
            sys.exit(0)
        print()


if __name__ == "__main__":
    main()
