import random

EVENTOS = [
    {
        "id": "voz_repetida",
        "titulo": "REPEATED VOICE",
        "descripcion": "You receive the same call as an hour ago. Same voice. Same words. Same number.",
        "detalle": "The log says that call never existed.",
        "efecto": "lucidez",
        "valor": -10,
    },
    {
        "id": "llamada_propia",
        "titulo": "YOUR OWN NUMBER",
        "descripcion": "A call comes in. The number is yours.",
        "detalle": "You don't pick up. The call lasts 47 seconds. There is breathing on the other end.",
        "efecto": "lucidez",
        "valor": -15,
    },
    {
        "id": "unidad_perdida",
        "titulo": "UNIT NOT RESPONDING",
        "descripcion": "The dispatched unit confirms arrival at the coordinates. Then, silence.",
        "detalle": "The GPS has it pinned at the same spot for 23 minutes. It is not moving.",
        "efecto": "lucidez",
        "valor": -12,
    },
    {
        "id": "grabacion_propia",
        "titulo": "ANOMALOUS RECORDING",
        "descripcion": "The system plays back a recording from two hours ago. Your voice is in the background.",
        "detalle": "You don't remember saying that. You don't remember that moment.",
        "efecto": "lucidez",
        "valor": -18,
    },
    {
        "id": "lucidez_repentina",
        "titulo": "MOMENT OF CLARITY",
        "descripcion": "For a second, everything makes sense. The calls, the coordinates, the pattern.",
        "detalle": "Then it's gone. But for a moment you saw it all.",
        "efecto": "lucidez",
        "valor": +20,
    },
    {
        "id": "cabina",
        "titulo": "UNIT REPORT",
        "descripcion": "The unit arrives at coordinates X=-9, Y=-9. It transmits a single message:",
        "detalle": '"There is a phone booth here. The receiver is off the hook."',
        "efecto": "lucidez",
        "valor": -20,
    },
    {
        "id": "llamada_saliente",
        "titulo": "UNREGISTERED OUTGOING CALL",
        "descripcion": "The system detects an outgoing call made 4 minutes ago. You didn't make it.",
        "detalle": "Or you don't remember.",
        "efecto": "lucidez",
        "valor": -10,
    },
    {
        "id": "señal_limpia",
        "titulo": "CLEAN SIGNAL",
        "descripcion": "For a few minutes, all frequencies are perfectly clean.",
        "detalle": "Too clean. As if something had stopped breathing.",
        "efecto": "lucidez",
        "valor": +10,
    },
    {
        "id": "coordenadas_imposibles",
        "titulo": "IMPOSSIBLE COORDINATES",
        "descripcion": "A call comes in from coordinates outside the operational range.",
        "detalle": "The system logs them. It shouldn't be able to.",
        "efecto": "pasos",
        "valor": -2,
    },
    {
        "id": "mensaje_pared",
        "titulo": "FRAGMENTED TRANSMISSION",
        "descripcion": "Through the static, someone says something. You only catch four words:",
        "detalle": '"I know you are listening"',
        "efecto": "lucidez",
        "valor": -15,
    },
]

def evento_aleatorio(probabilidad=0.35):
    if random.random() < probabilidad:
        return random.choice(EVENTOS)
    return None

def aplicar_evento(evento, operador):
    mensajes = []
    mensajes.append(f"\n  ⚠  EVENT — {evento['titulo']}")
    mensajes.append(f"  {evento['descripcion']}")
    mensajes.append(f"  {evento['detalle']}")

    if evento["efecto"] == "lucidez":
        operador.lucidez += evento["valor"]
        operador.lucidez = min(operador.lucidez, operador.lucidez_max)
        signo = "+" if evento["valor"] > 0 else ""
        mensajes.append(f"  >> Sanity {signo}{evento['valor']}.")
    elif evento["efecto"] == "pasos":
        operador.turnos_restantes += evento["valor"]
        mensajes.append(f"  >> Turns remaining {evento['valor']}.")

    operador.eventos_ocurridos.append(evento["titulo"])
    return mensajes
