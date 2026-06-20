# STATIC SIGNAL
> *Night shift. Frequency 156.8 MHz. You are the only one listening.*

You are an emergency radio operator on a night shift that starts behaving strangely. Something is moving out there. Survive until dawn.

---

## Requirements

- Python 3.11+
- No external dependencies — standard library only
- Sound on **Windows** only (`winsound`). The game runs normally on Mac/Linux, just without audio.
- Git is optional — only needed for `git clone`

---

## Installation

```bash
git clone https://github.com/soyelbengali/Static_Signal.git
```

Or click **Code → Download ZIP** and extract the folder.

---

## Running

```bash
python main.py
```

---

## Project structure

```
main.py       — Main loop and game logic
world.py      — Map, sectors, the signal, and their effects
player.py     — Operator (player) class
events.py     — Random events
map.py        — Visual radar and compass in terminal
report.py     — Final shift report
sound.py      — Sound module (Windows only)
README.md     — This file
```

---

## How to play

1. Enter your name and choose a difficulty.
2. Each turn shows the radar, your position, sanity, and time.
3. Move using compass directions: `n`, `s`, `e`, `w`, `ne`, `nw`, `se`, `sw`
4. Survive all turns without losing your sanity or getting caught.

---

## End conditions

| Condition | Result |
|---|---|
| Survive all turns | Victory |
| Sanity reaches 0 | Defeat — mental collapse |
| The monster catches you | Defeat — captured |
| Type `quit` | Abandoned |

---

## Map sectors

| Symbol | Type | Effect |
|---|---|---|
| `[◉]` | You | — |
| `[X]` | Signal | Visible only during pursuit |
| `[L]` | Call | Sanity −5 to −15 |
| `[S]` | Silence | Sanity −1 to −8 |
| `[I]` | Interference | Sanity −10 to −20, may attract the monster |
| `[R]` | Shelter | Sanity +8 to +20, 3 uses |
| `[?]` | Anomaly | Sanity −15 to −25, teleports you |
| `[C]` | Coffee | Sanity +5 to +12, 2 uses |
| `[D]` | Log | Sanity +8 to +15, 1 use |
| `[~]` | Old radio | Sanity +6 to +14, 2 uses |
| `[F]` | Photo | Sanity +10 to +18, 1 use |
| ` · ` | Unexplored | — |

---

## The Signal — monster behavior

The monster moves through three phases:

- **Patrol** `[x]` — moves randomly, unaware of your position. Invisible on radar.
- **Pursuit** `[X]` — charges directly toward you. Visible on radar; compass points at it.
- **Retreat** `[~]` — flees to the map edge. Cannot harm you. Invisible on radar.

**Pursuit is triggered when:**
- You come within 4 tiles (Manhattan distance)
- You enter a `[L]` Call sector (35% chance) or `[I]` Interference sector (55% chance)

Pursuit lasts 4–12 turns. Once it ends, the monster retreats and reappears at a random map edge.

---

## Special mechanics

- **Shift clock** — advances 7 minutes per turn, starting at 23:00.
- **Broken text** — below 20% sanity, sector messages become fragmented and strange.
- **Depleting sectors** — Shelter, Coffee, Log, Radio, and Photo have limited uses. Once exhausted, they become empty tiles.
- **Compass** — always points toward the monster. Shows exact distance and coordinates only during pursuit.

---

## Difficulty

| Level | Sanity | Turns | Event chance |
|---|---|---|---|
| Easy | 100 | 20 | 20% |
| Normal | 80 | 30 | 35% |
| Hard | 60 | 40 | 50% |
