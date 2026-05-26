import time
import random
from collections import Counter
from mapa import ROJO, ROJO_OSCURO, ROJO_FUERTE, NEGRITA, AMARILLO, GRIS, R

LINEA = "─" * 52

def pausar():
    time.sleep(0.04)

def imprimir_lento(texto, velocidad=0.03):
    for letra in texto:
        print(letra, end="", flush=True)
        time.sleep(velocidad)
    print()

def mostrar_informe(operador, config_inicial, veces_detectado=0):
    print()
    print(LINEA)
    print("  FINAL REPORT — SHIFT CLOSED")
    print(LINEA)
    time.sleep(0.3)

    print(f"  Operator        : {operador.nombre}")
    print(f"  Starting position: X={config_inicial['x']}, Y={config_inicial['y']}")
    print(f"  Starting sanity  : {config_inicial['lucidez']}")
    print(f"  Max turns        : {config_inicial['turnos']}")
    print()
    time.sleep(0.2)

    print(f"  Final position  : X={operador.x}, Y={operador.y}")
    print(f"  Turns completed : {operador.turnos_superados}")
    print(f"  Sanity remaining: {max(operador.lucidez, 0)}/{operador.lucidez_max}")
    print()
    time.sleep(0.2)

    if operador.eventos_ocurridos:
        print("  Logged events:")
        for ev in operador.eventos_ocurridos:
            print(f"    — {ev}")
    else:
        print("  Logged events: none.")
    print()

    if operador.sectores_visitados:
        conteo = Counter(tipo for _, _, tipo in operador.sectores_visitados)
        print("  Sectors visited:")
        for tipo, n in conteo.most_common():
            print(f"    — {tipo:15} x{n}")
    print()

    print(f"  Signal detections: {veces_detectado}")
    print()
    time.sleep(0.2)

    print(f"  Cause of closure: {operador.causa_fin}")
    print()
    print(LINEA)
    time.sleep(0.3)

    if operador.resultado == "victoria":
        print("  RESULT: SHIFT COMPLETED.")
        print()
        print("  You made it to dawn.")
        print("  The report has been sent.")
        print("  No one has confirmed receiving it.")

    elif operador.resultado in ("locura", "muerte"):
        if operador.resultado == "locura":
            print("  RESULT: OPERATOR COLLAPSE.")
        else:
            print("  RESULT: SIGNAL LOCATED. OPERATOR ELIMINATED.")
        print()

        fallos_sistema = [
            ("ERROR 174: OPERATIVE DISCONNECTION",              ROJO_OSCURO),
            ("ERROR 0x000A12: SIGNAL UNRECOVERABLE",            ROJO_OSCURO),
            ("CRITICAL ERROR: RETURN CODE -1",                  ROJO),
            ("FATAL ERROR: OPERATOR NOT RESPONDING",            ROJO_FUERTE),
            ("ERROR 502: SYNCHRONIZATION LOSS",                 ROJO_OSCURO),
            ("ERROR 31-B: FREQUENCY CORRUPTED",                 ROJO),
            ("SYSTEM ERROR: HUMAN INPUT INVALID",               ROJO),
            ("EXCEPTION RAISED: cognitive_overload()",          ROJO),
            ("KERNEL FAILURE: audio_stream_lost",               ROJO_FUERTE),
            ("ERROR 440: IDENTITY NOT VERIFIED",                ROJO_OSCURO),
            ("FATAL SIGNAL LOSS",                               ROJO),
            ("WARNING: operator out of range",                  AMARILLO),
            ("ERROR 7: transmission echo detected",             ROJO),
            ("STACK OVERFLOW: recursive_channel()",             ROJO_OSCURO),
            ("ERROR 991: multiple voices detected",             ROJO),
            ("RUNTIME ERROR: inconsistent coordinates",         ROJO_FUERTE),
            ("ERROR: unexpected call return",                   ROJO),
            ("BOOTH ERROR: microphone open without operator",   ROJO),
            ("ERROR 404: operator not found",                   ROJO_OSCURO),
            ("ERROR: signal continues after closure",           ROJO),
        ]

        pantalla_rota = random.sample(fallos_sistema, random.randint(4, 7))
        for mensaje, color in pantalla_rota:
            imprimir_lento(f"  {color}{mensaje}{R}", random.uniform(0.05, 0.09))
            time.sleep(random.uniform(0.05, 0.2))

        print()
        imprimir_lento("  signal lost", 0.06)
        imprimir_lento("  signal lost", 0.06)
        imprimir_lento("  signal lo", 0.08)
        time.sleep(0.4)
        print()

    elif operador.resultado == "tiempo":
        print("  RESULT: SHIFT ABANDONED.")
        print()
        print("  You left your post.")
        print("  The calls keep coming in.")
        print("  No one picks up.")

    print()
    print(LINEA)
