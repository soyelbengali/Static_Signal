RESET       = "\033[0m"
RED         = "\033[91m"
DARK_RED    = "\033[31m"
BRIGHT_RED  = "\033[91m\033[1m"
GREEN       = "\033[92m"
YELLOW      = "\033[93m"
BLUE        = "\033[94m"
MAGENTA     = "\033[95m"
CYAN        = "\033[96m"
WHITE       = "\033[97m"
GRAY        = "\033[90m"
BOLD        = "\033[1m"

RADAR_RADIUS = 5
RADAR_WIDTH  = 52

SECTOR_COLORS = {
    "empty":        GRAY,
    "call":         BLUE,
    "silence":      WHITE,
    "interference": RED,
    "shelter":      GREEN,
    "anomaly":      MAGENTA,
}

SECTOR_SYMBOLS = {
    "empty":        " · ",
    "call":         "[L]",
    "silence":      "[S]",
    "interference": "[I]",
    "shelter":      "[R]",
    "anomaly":      "[?]",
}

SIGNAL_SYMBOLS = {
    "patrol":  (GRAY,        "[x]"),
    "pursuit": (RED + BOLD,  "[X]"),
    "retreat": (YELLOW,      "[~]"),
}

PHASE_COLORS = {
    "patrol":  GRAY,
    "pursuit": RED + BOLD,
    "retreat": YELLOW,
}

PHASE_LABELS = {
    "patrol":  "PATROL",
    "pursuit": "PURSUIT",
    "retreat": "RETREAT",
}

COMPASS_POINTS = {
    (-1,-1):"NW", (0,-1):"N",  (1,-1):"NE",
    (-1, 0):"W",  (0, 0):"·",  (1, 0):"E",
    (-1, 1):"SW", (0, 1):"S",  (1, 1):"SE",
}


def sanity_bar(sanity, maximum, width=20):
    filled = int((max(sanity, 0) / maximum) * width)
    empty = width - filled
    ratio = sanity / maximum
    color = GREEN if ratio > 0.6 else (YELLOW if ratio > 0.3 else RED)
    bar = color + "█" * filled + GRAY + "░" * empty + RESET
    return f"[{bar}{RESET}] {max(sanity, 0)}/{maximum}"


def _signal_compass(operator, world):
    signal = world.signal
    phase = signal.phase

    lines = []
    lines.append(f"{BOLD}SIGNAL [X]{RESET}  {PHASE_COLORS[phase]}{PHASE_LABELS[phase]}{RESET}")

    dx = signal.x - operator.x
    dy = signal.y - operator.y
    dist = abs(dx) + abs(dy)
    sx = 1 if dx > 0 else (-1 if dx < 0 else 0)
    sy = 1 if dy > 0 else (-1 if dy < 0 else 0)
    active_point = (sx, -sy) if (dx != 0 or dy != 0) else None

    if phase == "pursuit":
        lines.append(f"{GRAY}dist: {dist} steps{RESET}")
    else:
        lines.append(f"{GRAY}position: unknown{RESET}")
    lines.append("")

    for gy in range(-1, 2):
        row = " "
        for gx in range(-1, 2):
            label = COMPASS_POINTS[(gx, gy)]
            if label == "·":
                row += CYAN + " ◉ " + RESET
            elif (gx, gy) == active_point:
                row += PHASE_COLORS[phase] + f"{label:>2} " + RESET
            else:
                row += GRAY + f"{label:>2} " + RESET
        lines.append(row)

    lines.append("")
    if phase == "pursuit":
        lines.append(f"{RED}X={signal.x} Y={signal.y}{RESET}")
    else:
        lines.append(f"{GRAY}???{RESET}")

    return lines


def draw_map(operator, world):
    cx, cy = operator.x, operator.y
    signal = world.signal
    lines = []

    lines.append(
        f"\n  {BOLD}OPERATIONAL RADAR{RESET} "
        f"— position: {CYAN}X={operator.x} Y={operator.y}{RESET}"
    )
    lines.append("")

    radar_rows = []
    for dy in range(RADAR_RADIUS, -RADAR_RADIUS - 1, -1):
        y = cy + dy
        row = f" {GRAY}{y:>4}{RESET} "
        for dx in range(-RADAR_RADIUS, RADAR_RADIUS + 1):
            x = cx + dx

            if x == signal.x and y == signal.y and signal.phase == "pursuit":
                color, symbol = SIGNAL_SYMBOLS["pursuit"]
                row += color + symbol + RESET
                continue

            if dx == 0 and dy == 0:
                row += BOLD + CYAN + "[◉]" + RESET
                continue

            if (x, y) in world.sectors:
                sector = world.sectors[(x, y)]
                color  = SECTOR_COLORS.get(sector.type, GRAY)
                symbol = SECTOR_SYMBOLS.get(sector.type, " · ")
                row   += color + symbol + RESET
            else:
                row += GRAY + " · " + RESET

        radar_rows.append(row)

    x_axis = "       "
    for dx in range(-RADAR_RADIUS, RADAR_RADIUS + 1):
        x_axis += f"{GRAY}{cx+dx:^4}{RESET}"
    radar_rows.append(x_axis)

    compass = _signal_compass(operator, world)

    total_rows = max(len(radar_rows), len(compass))
    for i in range(total_rows):
        left  = radar_rows[i] if i < len(radar_rows) else ""
        right = compass[i]    if i < len(compass)    else ""
        visible_width = len(left.encode().decode("utf-8"))
        padding = max(0, RADAR_WIDTH - visible_width + 8)
        lines.append(left + " " * padding + "   " + right)

    lines.append("")

    legend_items = [
        (CYAN,         "[◉]", "you"),
        (RED + BOLD,   "[X]", "danger"),
        (YELLOW,       "[~]", "retreat"),
        (GRAY,         "[x]", "patrol"),
        (BLUE,         "[L]", "call"),
        (WHITE,        "[S]", "silence"),
        (RED,          "[I]", "interference"),
        (GREEN,        "[R]", "shelter"),
        (MAGENTA,      "[?]", "anomaly"),
        (GRAY,         " · ", "unexplored"),
    ]
    legend_row = "  "
    for color, symbol, name in legend_items:
        legend_row += f"{color}{symbol}{RESET}{GRAY}={name}{RESET}  "
    lines.append(legend_row)

    lines.append("")
    lines.append(f"  Sanity  {sanity_bar(operator.sanity, operator.sanity_max)}")
    lines.append("")

    print("\n".join(lines))
