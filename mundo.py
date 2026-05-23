import random

LIMITE_MIN = -10
LIMITE_MAX = 10

SECTORES_RUIDOSOS = {"llamada", "interferencia"}
DISTANCIA_DETECCION = 4
PERSECUCION_MIN = 4
PERSECUCION_MAX = 12

TIPOS_SECTOR = {
    "vacio":          {"descripcion": "Sector sin actividad registrada.",                    "efecto": None},
    "llamada":        {"descripcion": "Señal de llamada activa.",                            "efecto": "llamada"},
    "silencio":       {"descripcion": "Zona de silencio total. Sin señal.",                  "efecto": "silencio"},
    "interferencia":  {"descripcion": "Interferencia severa. Los datos se corrompen.",       "efecto": "interferencia"},
    "refugio":        {"descripcion": "Estación repetidora. Señal estable.",                 "efecto": "refugio"},
    "anomalia":       {"descripcion": "Coordenada que no aparece en ningún mapa oficial.",   "efecto": "anomalia"},
    "cafe":           {"descripcion": "Máquina de café. Todavía funciona.",                  "efecto": "cafe"},
    "diario":         {"descripcion": "Alguien dejó un diario de turno aquí.",               "efecto": "diario"},
    "radio_vieja":    {"descripcion": "Una radio antigua emite música estática.",            "efecto": "radio_vieja"},
    "foto":           {"descripcion": "Una foto familiar. No recuerdas quién es.",           "efecto": "foto"},
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

# cuántos turnos aguanta un refugio/café/diario antes de agotarse
DURACION_SECTOR = {
    "refugio":     3,
    "cafe":        2,
    "diario":      1,
    "radio_vieja": 2,
    "foto":        1,
}

def generar_tipo_sector():
    tipos = [t for t, _ in PROBABILIDAD_SECTOR]
    pesos = [p for _, p in PROBABILIDAD_SECTOR]
    return random.choices(tipos, weights=pesos, k=1)[0]

def distancia(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)

class Sector:
    def __init__(self, x, y, tipo=None):
        self.x = x
        self.y = y
        self.tipo = tipo if tipo else generar_tipo_sector()
        self.visitado = False
        self.usos = 0

    def descripcion(self):
        tipo_real = self._tipo_actual()
        return TIPOS_SECTOR[tipo_real]["descripcion"]

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
            return True, f"distancia crítica ({dist} pasos)"
        if sector_tipo in SECTORES_RUIDOSOS:
            prob = 0.55 if sector_tipo == "interferencia" else 0.35
            if random.random() < prob:
                return True, f"ruido del sector [{sector_tipo.upper()}]"
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
        # borde aleatorio: norte, sur, este u oeste
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

        # marcar uso si es sector con duracion
        from mundo import DURACION_SECTOR
        if sector.tipo in DURACION_SECTOR:
            sector.usos += 1
            usos_restantes = DURACION_SECTOR[sector.tipo] - sector.usos
            if usos_restantes == 0:
                mensajes.append(f"  >> Este sector se ha agotado. Ya no volverá a funcionar.")
            elif usos_restantes == 1:
                mensajes.append(f"  >> Queda solo un uso más en este sector.")

        if efecto == "llamada":
            perdida = random.randint(5, 15)
            operador.lucidez -= perdida
            mensajes.append("  >> Llamada entrante. Voz irreconocible.")
            mensajes.append(f"  >> Lucidez -{perdida}.")

        elif efecto == "silencio":
            perdida = random.randint(1, 8)
            operador.lucidez -= perdida
            mensajes.append("  >> Silencio absoluto. Ni estática. Ni nada.")
            mensajes.append(f"  >> Lucidez -{perdida}.")

        elif efecto == "interferencia":
            perdida = random.randint(10, 20)
            operador.lucidez -= perdida
            mensajes.append("  >> INTERFERENCIA SEVERA. Registros corruptos.")
            mensajes.append(f"  >> Lucidez -{perdida}.")

        elif efecto == "refugio":
            ganancia = random.randint(8, 20)
            operador.lucidez += ganancia
            operador.lucidez = min(operador.lucidez, operador.lucidez_max)
            mensajes.append("  >> Estación repetidora activa. Señal limpia.")
            mensajes.append(f"  >> Lucidez +{ganancia}.")

        elif efecto == "anomalia":
            perdida = random.randint(15, 25)
            operador.lucidez -= perdida
            nx = random.randint(LIMITE_MIN, LIMITE_MAX)
            ny = random.randint(LIMITE_MIN, LIMITE_MAX)
            operador.x = nx
            operador.y = ny
            mensajes.append("  >> COORDENADA ANÓMALA.")
            mensajes.append(f"  >> Reubicado en X={nx}, Y={ny}.")
            mensajes.append(f"  >> Lucidez -{perdida}.")

        elif efecto == "cafe":
            ganancia = random.randint(5, 12)
            operador.lucidez += ganancia
            operador.lucidez = min(operador.lucidez, operador.lucidez_max)
            mensajes.append("  >> Café frío. Pero café.")
            mensajes.append(f"  >> Lucidez +{ganancia}. Te despejas un poco.")

        elif efecto == "diario":
            ganancia = random.randint(8, 15)
            operador.lucidez += ganancia
            operador.lucidez = min(operador.lucidez, operador.lucidez_max)
            frases = [
                "Alguien escribió: 'si lees esto, ya saben que estás aquí'.",
                "La última entrada dice: '03:41 — no respondas la línea 4'.",
                "Letra apretada: 'las coordenadas negativas no son reales. repito: no son reales'.",
                "Tinta borrosa: 'encontré el patrón. no sirve de nada'.",
            ]
            mensajes.append(f"  >> {random.choice(frases)}")
            mensajes.append(f"  >> Lucidez +{ganancia}. Saber que no eres el primero ayuda.")

        elif efecto == "radio_vieja":
            ganancia = random.randint(6, 14)
            operador.lucidez += ganancia
            operador.lucidez = min(operador.lucidez, operador.lucidez_max)
            canciones = [
                "Emite algo que suena a jazz. No identificas la canción.",
                "Una voz lee el tiempo de hace tres días.",
                "Música. Para. Música. Como si alguien cambiara el dial.",
                "Solo estática, pero rítmica. Casi confortante.",
            ]
            mensajes.append(f"  >> {random.choice(canciones)}")
            mensajes.append(f"  >> Lucidez +{ganancia}.")

        elif efecto == "foto":
            ganancia = random.randint(10, 18)
            operador.lucidez += ganancia
            operador.lucidez = min(operador.lucidez, operador.lucidez_max)
            detalles = [
                "Dos personas en una playa. Felices. El reverso dice 'agosto'.",
                "Un niño con un perro. La foto está quemada por un lado.",
                "Alguien frente a este mismo edificio. De día. Parece otro lugar.",
            ]
            mensajes.append(f"  >> {random.choice(detalles)}")
            mensajes.append(f"  >> Lucidez +{ganancia}. Te recuerda que había un antes.")

        return mensajes

TIPOS_SECTOR = {
    "vacio":          {"descripcion": "Sector sin actividad registrada.",                    "efecto": None},
    "llamada":        {"descripcion": "Señal de llamada activa.",                            "efecto": "llamada"},
    "silencio":       {"descripcion": "Zona de silencio total. Sin señal.",                  "efecto": "silencio"},
    "interferencia":  {"descripcion": "Interferencia severa. Los datos se corrompen.",       "efecto": "interferencia"},
    "refugio":        {"descripcion": "Estación repetidora. Señal estable.",                 "efecto": "refugio"},
    "anomalia":       {"descripcion": "Coordenada que no aparece en ningún mapa oficial.",   "efecto": "anomalia"},
}

PROBABILIDAD_SECTOR = [
    ("vacio",         35),
    ("llamada",       20),
    ("silencio",      10),
    ("interferencia", 15),
    ("refugio",       10),
    ("anomalia",       5),
]

def generar_tipo_sector():
    tipos = [t for t, _ in PROBABILIDAD_SECTOR]
    pesos = [p for _, p in PROBABILIDAD_SECTOR]
    return random.choices(tipos, weights=pesos, k=1)[0]

def distancia(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)

class Sector:
    def __init__(self, x, y, tipo=None):
        self.x = x
        self.y = y
        self.tipo = tipo if tipo else generar_tipo_sector()
        self.visitado = False

    def descripcion(self):
        return TIPOS_SECTOR[self.tipo]["descripcion"]

    def efecto(self):
        return TIPOS_SECTOR[self.tipo]["efecto"]

class Monstruo:
    
    def __init__(self):
        self.x = random.randint(LIMITE_MIN, LIMITE_MAX)
        self.y = random.randint(LIMITE_MIN, LIMITE_MAX)
        self.fase = "patrulla"
        self.turnos_persecucion = 0
        self.limite_persecucion = 0
        self.turnos_retirada = 0

    # detección
    def comprobar_deteccion(self, op, sector_tipo):
        
        dist = distancia(self.x, self.y, op.x, op.y)

        if self.fase == "retirada":
            return False, ""

        # por distancia
        if dist <= DISTANCIA_DETECCION:
            return True, f"distancia crítica ({dist} pasos)"

        # por ruido del sector
        if sector_tipo in SECTORES_RUIDOSOS:
            # probabilidad de que el ruido lo atraiga
            prob = 0.55 if sector_tipo == "interferencia" else 0.35
            if random.random() < prob:
                return True, f"ruido del sector [{sector_tipo.upper()}]"

        return False, ""

    # cambio de fase
    def iniciar_persecucion(self):
        self.fase = "persecucion"
        self.turnos_persecucion = 0
        self.limite_persecucion = random.randint(PERSECUCION_MIN, PERSECUCION_MAX)

    def iniciar_retirada(self):
        self.fase = "retirada"
        self.turnos_retirada = 0

    def volver_a_patrulla(self):
        self.fase = "patrulla"
        # reaparece en borde opuesto del mapa
        self.x = random.choice([LIMITE_MIN, LIMITE_MAX])
        self.y = random.randint(LIMITE_MIN, LIMITE_MAX)

    # movimiento
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
            # huye hacia el borde del mapa más cercano
            dx = -1 if self.x <= 0 else 1
            dy = -1 if self.y <= 0 else 1
            self.x += dx
            self.y += dy
            self.turnos_retirada += 1

            # salió del mapa → vuelve a patrullar desde el borde opuesto
            if (self.x < LIMITE_MIN or self.x > LIMITE_MAX or
                    self.y < LIMITE_MIN or self.y > LIMITE_MAX):
                self.volver_a_patrulla()

    def colision(self, op_x, op_y):
        # solo mata en persecución
        return self.fase == "persecucion" and self.x == op_x and self.y == op_y

    def dist_a(self, op_x, op_y):
        return distancia(self.x, self.y, op_x, op_y)


class Mundo:
    def __init__(self):
        self.sectores  = {}
        self.monstruo  = Monstruo()

    # acceso directo para compatibilidad con mapa.py
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

        if efecto == "llamada":
            perdida = random.randint(5, 15)
            operador.lucidez -= perdida
            mensajes.append("  >> Llamada entrante en este sector. Voz irreconocible.")
            mensajes.append(f"  >> Lucidez -{perdida}. Algo en esa voz no encajaba.")

        elif efecto == "silencio":
            perdida = random.randint(1, 8)
            operador.lucidez -= perdida
            mensajes.append("  >> Silencio absoluto. Ni estática. Ni nada.")
            mensajes.append(f"  >> Lucidez -{perdida}. El silencio es peor que el ruido.")

        elif efecto == "interferencia":
            perdida = random.randint(10, 20)
            operador.lucidez -= perdida
            mensajes.append("  >> INTERFERENCIA SEVERA. Los registros de este sector están corruptos.")
            mensajes.append(f"  >> Lucidez -{perdida}.")

        elif efecto == "refugio":
            ganancia = random.randint(8, 20)
            operador.lucidez += ganancia
            operador.lucidez = min(operador.lucidez, operador.lucidez_max)
            mensajes.append("  >> Estación repetidora activa. Señal limpia. Respiras.")
            mensajes.append(f"  >> Lucidez +{ganancia}.")

        elif efecto == "anomalia":
            perdida = random.randint(15, 25)
            operador.lucidez -= perdida
            nx = random.randint(LIMITE_MIN, LIMITE_MAX)
            ny = random.randint(LIMITE_MIN, LIMITE_MAX)
            operador.x = nx
            operador.y = ny
            mensajes.append("  >> COORDENADA ANÓMALA. Este punto no existe en los mapas oficiales.")
            mensajes.append(f"  >> La señal te arrastra. Reubicado en X={nx}, Y={ny}.")
            mensajes.append(f"  >> Lucidez -{perdida}.")

        return mensajes


# Textos alterados para lucidez baja
TEXTOS_ROTOS = {
    "vacio": [
        "  >> el sector está v a c í o",
        "  >> nada. nada. nada. nada.",
        "  >> sin actividad. o eso dice el sistema.",
    ],
    "llamada": [
        "  >> la voz dice tu nombre",
        "  >> no puedes colgar. sabes que no puedes colgar.",
        "  >> la llamada lleva abierta demasiado tiempo",
    ],
    "silencio": [
        "  >> demasiado silencio. algo lo está absorbiendo.",
        "  >> no hay señal. no hay nada. estás solo.",
        "  >> el silencio tiene forma",
    ],
    "interferencia": [
        "  >> los datos dicen que esto no está pasando",
        "  >> ERROR ERROR ERROR",
        "  >> alguien está grabando esto",
    ],
    "refugio": [
        "  >> la señal está limpia. tú no.",
        "  >> funciona. por ahora.",
        "  >> respiras. o algo que se parece a respirar.",
    ],
}

def texto_roto_sector(tipo):
    """Devuelve un mensaje alterado aleatorio para el tipo de sector dado."""
    opciones = TEXTOS_ROTOS.get(tipo, ["  >> ."])
    return __import__('random').choice(opciones)