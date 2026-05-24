import random

EVENTOS = [
    {
        "id": "voz_repetida",
        "titulo": "VOZ REPETIDA",
        "descripcion": "Recibes la misma llamada que hace una hora. Misma voz. Mismas palabras. Mismo número.",
        "detalle": "El registro dice que esa llamada nunca existió.",
        "efecto": "lucidez",
        "valor": -10,
    },
    {
        "id": "llamada_propia",
        "titulo": "NÚMERO PROPIO",
        "descripcion": "Entra una llamada. El número es el tuyo.",
        "detalle": "No descuelgas. La llamada dura 47 segundos. Hay respiración al otro lado.",
        "efecto": "lucidez",
        "valor": -15,
    },
    {
        "id": "unidad_perdida",
        "titulo": "UNIDAD SIN RESPUESTA",
        "descripcion": "La unidad despachada confirma llegada a las coordenadas. Después, silencio.",
        "detalle": "El GPS la sitúa en el mismo punto desde hace 23 minutos. No se mueve.",
        "efecto": "lucidez",
        "valor": -12,
    },
    {
        "id": "grabacion_propia",
        "titulo": "GRABACIÓN ANÓMALA",
        "descripcion": "El sistema reproduce una grabación de hace dos horas. Se escucha tu voz al fondo.",
        "detalle": "No recuerdas haber dicho eso. No recuerdas ese momento.",
        "efecto": "lucidez",
        "valor": -18,
    },
    {
        "id": "lucidez_repentina",
        "titulo": "MOMENTO DE CLARIDAD",
        "descripcion": "Por un segundo, todo tiene sentido. Las llamadas, las coordenadas, el patrón.",
        "detalle": "Luego se va. Pero por un momento lo viste todo.",
        "efecto": "lucidez",
        "valor": +20,
    },
    {
        "id": "cabina",
        "titulo": "INFORME DE UNIDAD",
        "descripcion": "La unidad llega a las coordenadas X=-9, Y=-9. Transmite un solo mensaje:",
        "detalle": '"Aquí hay una cabina. El teléfono está descolgado."',
        "efecto": "lucidez",
        "valor": -20,
    },
    {
        "id": "llamada_saliente",
        "titulo": "LLAMADA SALIENTE NO REGISTRADA",
        "descripcion": "El sistema detecta una llamada saliente hace 4 minutos. No la hiciste tú.",
        "detalle": "O no lo recuerdas.",
        "efecto": "lucidez",
        "valor": -10,
    },
    {
        "id": "señal_limpia",
        "titulo": "SEÑAL LIMPIA",
        "descripcion": "Durante unos minutos, todas las frecuencias están perfectamente limpias.",
        "detalle": "Demasiado limpias. Como si algo hubiera dejado de respirar.",
        "efecto": "lucidez",
        "valor": +10,
    },
    {
        "id": "coordenadas_imposibles",
        "titulo": "COORDENADAS IMPOSIBLES",
        "descripcion": "Entra una llamada desde coordenadas que están fuera del rango operativo.",
        "detalle": "El sistema las registra. No debería poder hacerlo.",
        "efecto": "pasos",
        "valor": -2,
    },
    {
        "id": "mensaje_pared",
        "titulo": "TRANSMISIÓN FRAGMENTADA",
        "descripcion": "Entre la estática, alguien dice algo. Solo capturas cuatro palabras:",
        "detalle": '"ya sé que escuchas"',
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
    mensajes.append(f"\n  ⚠  EVENTO — {evento['titulo']}")
    mensajes.append(f"  {evento['descripcion']}")
    mensajes.append(f"  {evento['detalle']}")

    if evento["efecto"] == "lucidez":
        operador.lucidez += evento["valor"]
        operador.lucidez = min(operador.lucidez, operador.lucidez_max)
        signo = "+" if evento["valor"] > 0 else ""
        mensajes.append(f"  >> Lucidez {signo}{evento['valor']}.")
    elif evento["efecto"] == "pasos":
        operador.turnos_restantes += evento["valor"]
        mensajes.append(f"  >> Turnos restantes {evento['valor']}.")

    operador.eventos_ocurridos.append(evento["titulo"])
    return mensajes