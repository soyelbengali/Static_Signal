import time
import random
from mapa import dibujar_mapa, ROJO, NEGRITA, AMARILLO, GRIS, R, VERDE, AZUL, MAGENTA, BLANCO, CYAN, ROJO_OSCURO, ROJO_FUERTE

LINEA = "─" * 52

def pausar():
    time.sleep(0.04)

def imprimir_lento(texto, pausa=0.03):
    import sys
    for c in texto:
        print(c, end="", flush=True)
        time.sleep(pausa)
    print()

def mostrar_informe(operador, params_iniciales, veces_detectado=0):
    print()
    print(LINEA)
    print("  INFORME FINAL — TURNO CERRADO")
    print(LINEA)
    time.sleep(0.3)

    print(f"  Operador       : {operador.nombre}")
    print(f"  Posición inicio: X={params_iniciales['x']}, Y={params_iniciales['y']}")
    print(f"  Lucidez inicio : {params_iniciales['lucidez']}")
    print(f"  Pasos máximos  : {params_iniciales['pasos']}")
    print()
    time.sleep(0.2)

    print(f"  Posición final : X={operador.x}, Y={operador.y}")
    print(f"  Pasos realizados: {operador.turnos_superados}")
    print(f"  Lucidez restante: {max(operador.lucidez, 0)}/{operador.lucidez_max}")
    print()
    time.sleep(0.2)

    if operador.eventos_ocurridos:
        print("  Eventos registrados:")
        for ev in operador.eventos_ocurridos:
            print(f"    — {ev}")
    else:
        print("  Eventos registrados: ninguno.")
    print()

    if operador.sectores_visitados:
        from collections import Counter
        conteo = Counter(tipo for _, _, tipo in operador.sectores_visitados)
        print("  Sectores visitados:")
        for tipo, n in conteo.most_common():
            print(f"    — {tipo:15} x{n}")
    print()

    print(f"  Detecciones por la señal: {veces_detectado}")
    print()
    time.sleep(0.2)

    print(f"  Causa de cierre: {operador.causa_fin}")
    print()
    print(LINEA)
    time.sleep(0.3)

    if operador.resultado == "victoria":
        print("  RESULTADO: TURNO COMPLETADO.")
        print()
        print("  Llegaste al amanecer.")
        print("  El informe ha sido enviado.")
        print("  Nadie ha confirmado recibirlo.")

    elif operador.resultado in ("locura", "muerte"):
        if operador.resultado == "locura":
            print("  RESULTADO: COLAPSO DEL OPERADOR.")
        else:
            print("  RESULTADO: SEÑAL LOCALIZADA. OPERADOR ELIMINADO.")
        print()

        ERRORES = [
            ("ERROR 174: DESCONEXIÓN OPERATIVA",                ROJO_OSCURO),
            ("ERROR 0x000A12: SEÑAL NO RECUPERABLE",            ROJO_OSCURO),
            ("ERROR CRÍTICO: RETURN CODE -1",                   ROJO),
            ("FATAL ERROR: OPERADOR NO RESPONDE",               ROJO_FUERTE),
            ("ERROR 502: PÉRDIDA DE SINCRONIZACIÓN",            ROJO_OSCURO),
            ("ERROR 31-B: FRECUENCIA CORRUPTA",                 ROJO),
            ("ERROR DE SISTEMA: INPUT HUMANO INVÁLIDO",         ROJO),
            ("EXCEPTION RAISED: cognitive_overload()",          ROJO),
            ("KERNEL FAILURE: audio_stream_lost",               ROJO_FUERTE),
            ("ERROR 440: IDENTIDAD NO VERIFICADA",              ROJO_OSCURO),
            ("FATAL SIGNAL LOSS",                               ROJO),
            ("WARNING: operador fuera de rango",                AMARILLO),
            ("ERROR 7: eco de transmisión detectado",           ROJO),
            ("STACK OVERFLOW: canal_recursivo()",               ROJO_OSCURO),
            ("ERROR 991: múltiples voces detectadas",           ROJO),
            ("RUNTIME ERROR: coordenadas inconsistentes",       ROJO_FUERTE),
            ("ERROR: retorno inesperado de llamada",            ROJO),
            ("ERROR DE CABINA: micrófono abierto sin operador", ROJO),
            ("ERROR 404: operador no encontrado",               ROJO_OSCURO),
            ("ERROR: la señal continúa después del cierre",     ROJO),
        ]

        seleccion = random.sample(ERRORES, random.randint(4, 7))
        for err, color in seleccion:
            imprimir_lento(f"  {color}{err}{R}", random.uniform(0.05, 0.09))
            time.sleep(random.uniform(0.05, 0.2))

    elif operador.resultado == "tiempo":
        print("  RESULTADO: TURNO ABANDONADO.")
        print()
        print("  Dejaste tu puesto.")
        print("  Las llamadas siguen entrando.")
        print("  Nadie las coge.")

    print()
    print(LINEA)