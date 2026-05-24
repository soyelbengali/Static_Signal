import random

LIMITE_MIN = -10
LIMITE_MAX = 10

SECTORES_RUIDOSOS = {"llamada", "interferencia"}
DISTANCIA_DETECCION = 4
PERSECUCION_MIN = 4
PERSECUCION_MAX = 12

TIPOS_SECTOR = {
    "vacio":         {"descripcion": "No activity recorded in this sector.",              "efecto": None},
    "llamada":       {"descripcion": "Active call signal.",                               "efecto": "llamada"},
    "silencio":      {"descripcion": "Zone of total silence. No signal.",                 "efecto": "silencio"},
    "interferencia": {"descripcion": "Severe interference. Data is corrupted.",           "efecto": "interferencia"},
    "refugio":       {"descripcion": "Repeater station. Stable signal.",                  "efecto": "refugio"},
    "anomalia":      {"descripcion": "Coordinate that appears on no official map.",       "efecto": "anomalia"},
    "cafe":          {"descripcion": "Coffee machine. Still working.",                    "efecto": "cafe"},
    "diario":        {"descripcion": "Someone left a shift log here.",                    "efecto": "diario"},
    "radio_vieja":   {"descripcion": "An old radio playing static music.",                "efecto": "radio_vieja"},
    "foto":          {"descripcion": "A family photo. You don't remember who they are.",  "efecto": "foto"},
}

PROBABILIDAD_SECTOR = [
    ("vacio",         30),
    ("llamada",       18),
    ("silencio",       8),
    ("interferencia", 13),
    ("refugio",        8),
    ("anomalia",       5),
    ("cafe",           7),
    ("diario",         5),
    ("radio_vieja",    4),
    ("foto",           2),
]

DURACION_SECTOR = {
    "refugio":     3,
    "cafe":        2,
    "diario":      1,
    "radio_vieja": 2,
    "foto":        1,
}

TEXTOS_ROTOS = {
    "vacio": [
        "  >> the sector is e m p t y",
        "  >> nothing. nothing. nothing. nothing.",
        "  >> no activity. that's what the system says.",
    ],
    "llamada": [
        "  >> the voice says your name",
        "  >> you can't hang up. you know you can't hang up.",
        "  >> the call has been open for too long",
    ],
    "silencio": [
        "  >> too much silence. something is absorbing it.",
        "  >> no signal. nothing. you are alone.",
        "  >> the silence has a shape",
    ],
    "interferencia": [
        "  >> the data says this is not happening",
        "  >> ERROR ERROR ERROR",
        "  >> someone is recording this",
    ],
    "refugio": [
        "  >> the signal is clean. you are not.",
        "  >> it works. for now.",
        "  >> you breathe. or something that resembles breathing.",
    ],
    "cafe": [
        "  >> the coffee tastes like something that isn't coffee",
        "  >> you drink it anyway",
    ],
    "diario": [
        "  >> the handwriting is yours. you don't remember writing it.",
        "  >> the last page is blank. or almost.",
    ],
    "radio_vieja": [
        "  >> the song ends. it starts again from the beginning.",
        "  >> someone is singing on a frequency that shouldn't exist.",
    ],
    "foto": [
        "  >> the person in the photo is looking at you.",
        "  >> there is someone behind them. you hadn't noticed before.",
    ],
}


def generar_tipo_sector():
    tipos = [t for t, _ in PROBABILIDAD_SECTOR]
    pesos = [p for _, p in PROBABILIDAD_SECTOR]
    return random.choices(tipos, weights=pesos, k=1)[0]

def distancia(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)

def texto_roto_sector(tipo):
    opciones = TEXTOS_ROTOS.get(tipo, ["  >> ."])
    return random.choice(opciones)


class Sector:
    def __init__(self, x, y, tipo=None):
        self.x = x
        self.y = y
        self.tipo = tipo if tipo else generar_tipo_sector()
        self.visitado = False
        self.usos = 0

    def descripcion(self):
        return TIPOS_SECTOR[self._tipo_actual()]["descripcion"]

    def efecto(self):
        return TIPOS_SECTOR[self._tipo_actual()]["efecto"]

    def _tipo_actual(self):
        duracion = DURACION_SECTOR.get(self.tipo)
        if duracion is not None and self.usos >= duracion:
            return "vacio"
        return self.tipo

    def tipo_visible(self):
        return self._tipo_actual()


class Monstruo:
    def __init__(self):
        self.x = random.randint(LIMITE_MIN, LIMITE_MAX)
        self.y = random.randint(LIMITE_MIN, LIMITE_MAX)
        self.fase = "patrulla"
        self.turnos_persecucion = 0
        self.limite_persecucion = 0
        self.turnos_retirada = 0
        self.veces_detectado = 0

    def comprobar_deteccion(self, op, sector_tipo):
        dist = distancia(self.x, self.y, op.x, op.y)
        if self.fase == "retirada":
            return False, ""
        if dist <= DISTANCIA_DETECCION:
            return True, f"critical distance ({dist} steps)"
        if sector_tipo in SECTORES_RUIDOSOS:
            prob = 0.55 if sector_tipo == "interferencia" else 0.35
            if random.random() < prob:
                return True, f"sector noise [{sector_tipo.upper()}]"
        return False, ""

    def iniciar_persecucion(self):
        self.fase = "persecucion"
        self.turnos_persecucion = 0
        self.limite_persecucion = random.randint(PERSECUCION_MIN, PERSECUCION_MAX)
        self.veces_detectado += 1

    def iniciar_retirada(self):
        self.fase = "retirada"
        self.turnos_retirada = 0

    def volver_a_patrulla(self):
        self.fase = "patrulla"
        borde = random.choice(["N", "S", "E", "O"])
        if borde == "N":
            self.x = random.randint(LIMITE_MIN, LIMITE_MAX)
            self.y = LIMITE_MAX
        elif borde == "S":
            self.x = random.randint(LIMITE_MIN, LIMITE_MAX)
            self.y = LIMITE_MIN
        elif borde == "E":
            self.x = LIMITE_MAX
            self.y = random.randint(LIMITE_MIN, LIMITE_MAX)
        else:
            self.x = LIMITE_MIN
            self.y = random.randint(LIMITE_MIN, LIMITE_MAX)

    def mover(self, op_x, op_y):
        if self.fase == "patrulla":
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            self.x = max(LIMITE_MIN, min(LIMITE_MAX, self.x + dx))
            self.y = max(LIMITE_MIN, min(LIMITE_MAX, self.y + dy))

        elif self.fase == "persecucion":
            if self.x < op_x:   self.x += 1
            elif self.x > op_x: self.x -= 1
            if self.y < op_y:   self.y += 1
            elif self.y > op_y: self.y -= 1
            self.turnos_persecucion += 1
            if self.turnos_persecucion >= self.limite_persecucion:
                self.iniciar_retirada()

        elif self.fase == "retirada":
            dx = -1 if self.x <= 0 else 1
            dy = -1 if self.y <= 0 else 1
            self.x += dx
            self.y += dy
            self.turnos_retirada += 1
            if (self.x < LIMITE_MIN or self.x > LIMITE_MAX or
                    self.y < LIMITE_MIN or self.y > LIMITE_MAX):
                self.volver_a_patrulla()

    def colision(self, op_x, op_y):
        return self.fase == "persecucion" and self.x == op_x and self.y == op_y

    def dist_a(self, op_x, op_y):
        return distancia(self.x, self.y, op_x, op_y)


class Mundo:
    def __init__(self):
        self.sectores = {}
        self.monstruo = Monstruo()

    @property
    def monstruo_x(self): return self.monstruo.x
    @property
    def monstruo_y(self): return self.monstruo.y
    @property
    def fase_monstruo(self): return self.monstruo.fase

    def obtener_sector(self, x, y):
        if (x, y) not in self.sectores:
            self.sectores[(x, y)] = Sector(x, y)
        return self.sectores[(x, y)]

    def dentro_de_limites(self, x, y):
        return LIMITE_MIN <= x <= LIMITE_MAX and LIMITE_MIN <= y <= LIMITE_MAX

    def aplicar_efecto(self, sector, operador):
        efecto = sector.efecto()
        mensajes = []

        if sector.tipo in DURACION_SECTOR:
            sector.usos += 1
            usos_restantes = DURACION_SECTOR[sector.tipo] - sector.usos
            if usos_restantes == 0:
                mensajes.append("  >> This sector is depleted. It won't work again.")
            elif usos_restantes == 1:
                mensajes.append("  >> Only one use left in this sector.")

        if efecto == "llamada":
            perdida = random.randint(5, 15)
            operador.lucidez -= perdida
            mensajes.append("  >> Incoming call. Unrecognizable voice.")
            mensajes.append(f"  >> Sanity -{perdida}.")

        elif efecto == "silencio":
            perdida = random.randint(1, 8)
            operador.lucidez -= perdida
            mensajes.append("  >> Total silence. No static. Nothing.")
            mensajes.append(f"  >> Sanity -{perdida}.")

        elif efecto == "interferencia":
            perdida = random.randint(10, 20)
            operador.lucidez -= perdida
            mensajes.append("  >> SEVERE INTERFERENCE. Records corrupted.")
            mensajes.append(f"  >> Sanity -{perdida}.")

        elif efecto == "refugio":
            ganancia = random.randint(8, 20)
            operador.lucidez += ganancia
            operador.lucidez = min(operador.lucidez, operador.lucidez_max)
            mensajes.append("  >> Repeater station active. Clean signal.")
            mensajes.append(f"  >> Sanity +{ganancia}.")

        elif efecto == "anomalia":
            perdida = random.randint(15, 25)
            operador.lucidez -= perdida
            nx = random.randint(LIMITE_MIN, LIMITE_MAX)
            ny = random.randint(LIMITE_MIN, LIMITE_MAX)
            operador.x = nx
            operador.y = ny
            mensajes.append("  >> ANOMALOUS COORDINATE.")
            mensajes.append(f"  >> The signal pulls you. Relocated to X={nx}, Y={ny}.")
            mensajes.append(f"  >> Sanity -{perdida}.")

        elif efecto == "cafe":
            ganancia = random.randint(5, 12)
            operador.lucidez += ganancia
            operador.lucidez = min(operador.lucidez, operador.lucidez_max)
            mensajes.append("  >> Cold coffee. But coffee.")
            mensajes.append(f"  >> Sanity +{ganancia}. You clear your head a little.")

        elif efecto == "diario":
            ganancia = random.randint(8, 15)
            operador.lucidez += ganancia
            operador.lucidez = min(operador.lucidez, operador.lucidez_max)
            frases = [
                "Someone wrote: 'if you read this, they already know you are here'.",
                "Last entry: '03:41 — do not answer line 4'.",
                "Tight handwriting: 'the negative coordinates are not real. repeat: not real'.",
                "Smudged ink: 'I found the pattern. It doesn't help'.",
            ]
            mensajes.append(f"  >> {random.choice(frases)}")
            mensajes.append(f"  >> Sanity +{ganancia}. Knowing you're not the first helps.")

        elif efecto == "radio_vieja":
            ganancia = random.randint(6, 14)
            operador.lucidez += ganancia
            operador.lucidez = min(operador.lucidez, operador.lucidez_max)
            canciones = [
                "Something that sounds like jazz. You can't place the song.",
                "A voice reading the weather from three days ago.",
                "Music. Stops. Music. As if someone were changing the dial.",
                "Just static, but rhythmic. Almost comforting.",
            ]
            mensajes.append(f"  >> {random.choice(canciones)}")
            mensajes.append(f"  >> Sanity +{ganancia}.")

        elif efecto == "foto":
            ganancia = random.randint(10, 18)
            operador.lucidez += ganancia
            operador.lucidez = min(operador.lucidez, operador.lucidez_max)
            detalles = [
                "Two people on a beach. Happy. The back says 'August'.",
                "A child with a dog. The photo is burned on one side.",
                "Someone standing in front of this very building. Daytime. It looks like another place.",
            ]
            mensajes.append(f"  >> {random.choice(detalles)}")
            mensajes.append(f"  >> Sanity +{ganancia}. It reminds you there was a before.")

        return mensajes
