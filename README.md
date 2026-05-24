# STATIC SIGNAL

> Night shift. Frequency 156.8 MHz. You are the only one listening.

You are an emergency radio operator on a night shift that starts behaving strangely. Something is moving out there. Survive until dawn.

---

## Requirements

- Python 3.11 or higher
- No external dependencies — standard Python library only
- Sound works on **Windows** only (winsound). On Mac/Linux the game runs normally but without audio.

---

## How to run

```bash
python main.py
```

Place the sound files `staticshort.wav` and `heartbeatshort.wav` in the same folder as `main.py`.

---

## Project files

```
main.py       — Main loop and game logic
mundo.py      — Map, sectors, monster and their effects
operador.py   — Player character class
eventos.py    — Random events
mapa.py       — Visual radar and compass in terminal
informe.py    — Final shift report
sonido.py     — Sound module (winsound, Windows only)
README.md     — This file
```

---

## How to play

1. Enter your name and choose a difficulty.
2. Each turn shows the radar, your position, sanity and time.
3. Choose a direction to move: `n`, `s`, `e`, `w`, `ne`, `nw`, `se`, `sw`
4. Survive all turns without losing your sanity or getting caught.

---

## End conditions

| Condition | Result |
|---|---|
| Survive all turns | Victory |
| Sanity reaches 0 | Defeat — collapse |
| The monster catches you | Defeat — captured |
| Type `quit` | Abandoned |

---

## Map sectors

| Symbol | Type | Effect |
|---|---|---|
| `[◉]` | You | — |
| `[X]` | Signal (monster) | Visible only during pursuit |
| `[L]` | Call | Sanity −5 to −15 |
| `[S]` | Silence | Sanity −1 to −8 |
| `[I]` | Interference | Sanity −10 to −20, may attract the monster |
| `[R]` | Shelter | Sanity +8 to +20, lasts 3 uses |
| `[?]` | Anomaly | Sanity −15 to −25, teleports you |
| `[C]` | Coffee | Sanity +5 to +12, lasts 2 uses |
| `[D]` | Log | Sanity +8 to +15, lasts 1 use |
| `[~]` | Old radio | Sanity +6 to +14, lasts 2 uses |
| `[F]` | Photo | Sanity +10 to +18, lasts 1 use |
| ` · ` | Unexplored | — |

---

## The signal — monster behavior

The monster has three phases:

- **Patrol** `[x]` grey — moves randomly, does not know where you are. Invisible on the radar.
- **Pursuit** `[X]` red — comes straight for you. Visible on the radar. The compass points toward it.
- **Retreat** `[~]` yellow — flees toward the edge of the map. Cannot kill you. Invisible on the radar.

Pursuit is triggered if:
- You get within 4 steps or less (Manhattan distance)
- You step on a `[L]` call sector (35% chance) or `[I]` interference sector (55% chance)

Pursuit lasts between 4 and 12 random turns. Once it ends, the monster retreats and reappears at a random edge of the map.

---

## Special mechanics

- **Shift time** — the clock advances 7 minutes per turn. Starts at 23:00.
- **Broken text** — below 20% sanity, sector messages become fragmented and strange.
- **Sectors that deplete** — shelter, coffee, log, radio and photo have a limited number of uses. Once depleted they become empty sectors.
- **Compass** — always points toward the monster. Only shows distance and exact coordinates during pursuit.

---

## Difficulty

| Level | Sanity | Turns | Event chance |
|---|---|---|---|
| Easy | 100 | 20 | 20% |
| Normal | 80 | 30 | 35% |
| Hard | 60 | 40 | 50% |
