# Colores ANSI
R        = "\033[0m"
ROJO     = "\033[91m"
ROJO_OSCURO = "\033[31m"
ROJO_FUERTE  = "\033[91m\033[1m"
VERDE    = "\033[92m"
AMARILLO = "\033[93m"
AZUL     = "\033[94m"
MAGENTA  = "\033[95m"
CYAN     = "\033[96m"
BLANCO   = "\033[97m"
GRIS     = "\033[90m"
NEGRITA  = "\033[1m"

RADIO = 5

COLOR_SECTOR = {
    "vacio":         GRIS,
    "llamada":       AZUL,
    "silencio":      BLANCO,
    "interferencia": ROJO,
    "refugio":       VERDE,
    "anomalia":      MAGENTA,
}

SIMBOLO_SECTOR = {
    "vacio":         " · ",
    "llamada":       "[L]",
    "silencio":      "[S]",
    "interferencia": "[I]",
    "refugio":       "[R]",
    "anomalia":      "[?]",
}

# Símbolo del monstruo según su fase
SIMBOLO_MONSTRUO = {
    "patrulla":    (GRIS,            "[x]"),
    "persecucion": (ROJO + NEGRITA,  "[X]"),
    "retirada":    (AMARILLO,        "[~]"),
}

def barra_lucidez(lucidez, maximo, ancho=20):
    llenos = int((max(lucidez, 0) / maximo) * ancho)
    vacios = ancho - llenos
    pct = lucidez / maximo
    color = VERDE if pct > 0.6 else (AMARILLO if pct > 0.3 else ROJO)
    barra = color + "█" * llenos + GRIS + "░" * vacios + R
    return f"[{barra}{R}] {max(lucidez, 0)}/{maximo}"


def _compas_monstruo(op, mundo):
    """
    Brújula de 3×3.
    - Persecución: apunta hacia el monstruo, muestra distancia y coordenadas.
    - Patrulla / retirada: todos los puntos apagados, señal desconocida.
    """
    fase = mundo.fase_monstruo
    color_label = {"patrulla": GRIS, "persecucion": ROJO + NEGRITA, "retirada": AMARILLO}
    etiqueta_fase = {"patrulla": "PATRULLA", "persecucion": "PERSECUCIÓN", "retirada": "RETIRADA"}

    PUNTOS = {
        (-1,-1):"NO", (0,-1):"N",  (1,-1):"NE",
        (-1, 0):"O",  (0, 0):"·",  (1, 0):"E",
        (-1, 1):"SO", (0, 1):"S",  (1, 1):"SE",
    }

    lineas = []
    lineas.append(f"{NEGRITA}SEÑAL [X]{R}  {color_label[fase]}{etiqueta_fase[fase]}{R}")

    mx, my = mundo.monstruo_x, mundo.monstruo_y
    dx = mx - op.x
    dy = my - op.y
    dist = abs(dx) + abs(dy)
    sx = 1 if dx > 0 else (-1 if dx < 0 else 0)
    sy = 1 if dy > 0 else (-1 if dy < 0 else 0)
    activo = (sx, -sy) if (dx != 0 or dy != 0) else None

    color_flecha = {
        "patrulla":    GRIS,
        "persecucion": ROJO + NEGRITA,
        "retirada":    AMARILLO,
    }[fase]

    if fase == "persecucion":
        lineas.append(f"{GRIS}dist: {dist} pasos{R}")
    else:
        lineas.append(f"{GRIS}posición: desconocida{R}")
    lineas.append("")

    for gy in range(-1, 2):
        fila = " "
        for gx in range(-1, 2):
            etiq = PUNTOS[(gx, gy)]
            if etiq == "·":
                fila += CYAN + " ◉ " + R
            elif (gx, gy) == activo:
                fila += color_flecha + f"{etiq:>2} " + R
            else:
                fila += GRIS + f"{etiq:>2} " + R
        lineas.append(fila)

    lineas.append("")
    if fase == "persecucion":
        lineas.append(f"{ROJO}X={mx} Y={my}{R}")
    else:
        lineas.append(f"{GRIS}???{R}")

    return lineas


def dibujar_mapa(op, mundo):
    cx, cy = op.x, op.y
    lineas = []

    lineas.append(
        f"\n  {NEGRITA}RADAR OPERATIVO{R} "
        f"— posición: {CYAN}X={op.x} Y={op.y}{R}"
    )
    lineas.append("")

    # radar
    radar = []
    for dy in range(RADIO, -RADIO - 1, -1):
        y = cy + dy
        fila = f" {GRIS}{y:>4}{R} "
        for dx in range(-RADIO, RADIO + 1):
            x = cx + dx

            # monstruo — solo visible en persecución
            if (x == mundo.monstruo_x and y == mundo.monstruo_y
                    and mundo.fase_monstruo == "persecucion"):
                color_m, simbolo_m = SIMBOLO_MONSTRUO["persecucion"]
                fila += color_m + simbolo_m + R
                continue

            # jugador
            if dx == 0 and dy == 0:
                fila += NEGRITA + CYAN + "[◉]" + R
                continue

            # sector conocido
            if (x, y) in mundo.sectores:
                sector = mundo.sectores[(x, y)]
                color  = COLOR_SECTOR.get(sector.tipo, GRIS)
                simb   = SIMBOLO_SECTOR.get(sector.tipo, " · ")
                fila  += color + simb + R
            else:
                fila += GRIS + " · " + R

        radar.append(fila)

    # eje X
    eje = "       "
    for dx in range(-RADIO, RADIO + 1):
        eje += f"{GRIS}{cx+dx:^4}{R}"
    radar.append(eje)

    # brújula
    compas = _compas_monstruo(op, mundo)

    # combinar lado a lado
    ANCHO_RADAR = 52   # caracteres visibles de cada fila de radar
    total = max(len(radar), len(compas))
    for i in range(total):
        izq = radar[i]  if i < len(radar)  else ""
        der = compas[i] if i < len(compas) else ""
        # pad sin contar códigos ANSI
        visible = len(izq.encode().decode("utf-8"))
        pad = max(0, ANCHO_RADAR - visible + 8)
        lineas.append(izq + " " * pad + "   " + der)

    lineas.append("")

    # leyenda
    items = [
        (CYAN,            "[◉]", "tú"),
        (ROJO + NEGRITA,  "[X]", "peligro"),
        (AMARILLO,        "[~]", "retirada"),
        (GRIS,            "[x]", "patrulla"),
        (AZUL,            "[L]", "llamada"),
        (BLANCO,          "[S]", "silencio"),
        (ROJO,            "[I]", "interferencia"),
        (VERDE,           "[R]", "refugio"),
        (MAGENTA,         "[?]", "anomalía"),
        (GRIS,            " · ", "sin explorar"),
    ]
    fila_ley = "  "
    for color, simb, nombre in items:
        fila_ley += f"{color}{simb}{R}{GRIS}={nombre}{R}  "
    lineas.append(fila_ley)

    lineas.append("")
    lineas.append(f"  Lucidez  {barra_lucidez(op.lucidez, op.lucidez_max)}")
    lineas.append("")

    print("\n".join(lineas))
