import random
import time
import sys

from mundo import Mundo, LIMITE_MIN, LIMITE_MAX, texto_roto_sector
from operador import Operador
from eventos import evento_aleatorio, aplicar_evento
from informe import mostrar_informe, LINEA, pausar
from mapa import dibujar_mapa, ROJO, NEGRITA, AMARILLO, GRIS, R
import sonido

MOVIMIENTOS = {
    "n":  ( 0,  1), "s":  ( 0, -1),
    "e":  ( 1,  0), "o":  (-1,  0),
    "ne": ( 1,  1), "no": (-1,  1),
    "se": ( 1, -1), "so": (-1, -1),
}

ALIAS_MOVIMIENTO = {
    "norte": "n", "arriba": "n",
    "sur":   "s", "abajo":  "s",
    "este":  "e", "derecha":"e",
    "oeste": "o", "izquierda":"o",
}

NIVELES = {
    "1": {"nombre": "fácil",   "lucidez": 100, "turnos": 20, "prob_evento": 0.20},
    "2": {"nombre": "normal",  "lucidez":  80, "turnos": 30, "prob_evento": 0.35},
    "3": {"nombre": "difícil", "lucidez":  60, "turnos": 40, "prob_evento": 0.50},
}

SONIDOS_EVENTO = {
    "voz_repetida":           sonido.sonido_voz_repetida,
    "llamada_propia":         sonido.sonido_numero_propio,
    "unidad_perdida":         sonido.sonido_unidad_perdida,
    "grabacion_propia":       sonido.sonido_grabacion,
    "lucidez_repentina":      sonido.sonido_momento_claridad,
    "cabina":                 sonido.sonido_unidad_perdida,
    "llamada_saliente":       sonido.sonido_voz_repetida,
    "señal_limpia":           sonido.sonido_señal_limpia,
    "coordenadas_imposibles": sonido.sonido_coordenadas_imposibles,
    "mensaje_pared":          sonido.sonido_transmision_fragmentada,
}


def pausa(t=0.3):
    time.sleep(t)


def pedir_entero(pregunta, minimo, maximo, defecto=None):
    while True:
        entrada = input(pregunta).strip()
        if entrada == "" and defecto is not None:
            return defecto
        try:
            valor = int(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f"  Introduce un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  Valor no válido.")


def pedir_nombre(pregunta, defecto="Operador"):
    entrada = input(pregunta).strip()
    return entrada if entrada else defecto


def pantalla_inicio():
    print()
    print(LINEA)
    print()
    pausa(0.2)
    print("  SEÑAL ESTÁTICA")
    pausa(0.1)
    frecuencia = round(random.uniform(150.0, 160.0), 1)
    print(f"  Turno de noche. Frecuencia {frecuencia} MHz.")
    pausa(0.1)
    print("  Tú eres el único que escucha.")
    print()
    pausa(0.3)
    print(LINEA)
    pausa(0.4)
    print()
    print("  Llevas tres años haciendo el turno de noche.")
    print("  Sabes distinguir una borrachera de una emergencia real.")
    print("  Sabes cuándo alguien llora de verdad.")
    print()
    print("  Esta noche algo es diferente.")
    print()
    pausa(0.5)
    print(LINEA)
    print()


def configurar_turno():
    print("  CONFIGURACIÓN DEL TURNO")
    print()
    nombre_operador = pedir_nombre("  Nombre del operador (Enter = 'Operador'): ")
    print()
    print("  Dificultad:")
    for clave, nivel in NIVELES.items():
        print(f"    {clave}. {nivel['nombre']:8} — lucidez {nivel['lucidez']}, turnos {nivel['turnos']}")
    eleccion = input("  Elige (1/2/3, Enter = 2): ").strip()
    if eleccion not in NIVELES:
        eleccion = "2"
    nivel_elegido = NIVELES[eleccion]
    print()
    print(LINEA)
    print()
    print(f"  Operador        : {nombre_operador}")
    print(f"  Posición inicio : X=0, Y=0")
    print(f"  Lucidez         : {nivel_elegido['lucidez']}")
    print(f"  Turnos objetivo : {nivel_elegido['turnos']}")
    print(f"  Dificultad      : {nivel_elegido['nombre']}")
    print()
    print(f"  Área operativa  : X=[{LIMITE_MIN},{LIMITE_MAX}]  Y=[{LIMITE_MIN},{LIMITE_MAX}]")
    print("  Victoria  : sobrevivir todos los turnos")
    print("  Derrota   : lucidez=0 / atrapado / abandonar")
    print()
    print(LINEA)
    print()
    return nombre_operador, nivel_elegido


def mostrar_turno(operador, mundo, numero_turno, turnos_totales):
    print(f"\n  — TURNO {numero_turno}/{turnos_totales}   {operador.hora_actual()} —")
    dibujar_mapa(operador, mundo)
    print(f"  Estado mental    : [{operador.estado_lucidez()}]")
    print(f"  Turnos restantes : {operador.turnos_restantes}")


def pedir_direccion():
    print()
    print("  Direcciones: n / s / e / o / ne / no / se / so")
    print("  ('salir' para abandonar el turno)")
    while True:
        entrada = input("  > ").strip().lower()
        if entrada == "salir":
            return None
        entrada = ALIAS_MOVIMIENTO.get(entrada, entrada)
        if entrada in MOVIMIENTOS:
            return entrada
        print("  Dirección no reconocida.")


def simular_turno(operador, mundo, nivel):
    turnos_totales = nivel["turnos"]
    prob_evento = nivel["prob_evento"]
    config_inicial = {
        "x": operador.x, "y": operador.y,
        "lucidez": operador.lucidez_max,
        "turnos": operador.turnos_restantes,
    }

    numero_turno = 0

    while operador.esta_vivo():
        numero_turno += 1

        if numero_turno > turnos_totales:
            operador.resultado = "victoria"
            operador.causa_fin = "Supervivencia completada"
            sonido.sonido_victoria()
            break

        mostrar_turno(operador, mundo, numero_turno, turnos_totales)
        operador.avanzar_hora(7)

        zona_actual = mundo.obtener_sector(operador.x, operador.y)
        if not zona_actual.visitado:
            zona_actual.visitado = True
            operador.sectores_visitados.append((operador.x, operador.y, zona_actual.tipo_visible()))
            sonido.sonido_sector(zona_actual.tipo)

        tipo_zona = zona_actual.tipo_visible()
        print(f"  Sector  : {tipo_zona.upper()} — {zona_actual.descripcion()}")

        if operador.alucinando():
            print(texto_roto_sector(tipo_zona))

        efectos = mundo.aplicar_efecto(zona_actual, operador)
        for linea in efectos:
            print(linea)
            pausa(0.04)

        if not operador.esta_vivo():
            break

        señal = mundo.monstruo
        fase_anterior = señal.fase

        detectado, motivo = señal.comprobar_deteccion(operador, zona_actual.tipo)
        if detectado and señal.fase == "patrulla":
            señal.iniciar_persecucion()
            sonido.sonido_deteccion()
            print(f"\n  {ROJO}{NEGRITA}⚠  SEÑAL DETECTADA — {motivo.upper()}{R}")
            print(f"  {ROJO}Algo viene hacia ti.{R}")
            pausa(0.2)

        señal.mover(operador.x, operador.y)

        if señal.fase != fase_anterior:
            if señal.fase == "retirada":
                print(f"\n  {AMARILLO}  La señal pierde tu rastro. Se aleja.{R}")
                sonido.reanudar_estatico()
            elif señal.fase == "patrulla":
                print(f"\n  {GRIS}  Silencio. La señal vuelve a vagar.{R}")

        if señal.colision(operador.x, operador.y):
            sonido.pausar_estatico()
            sonido.sonido_muerte()
            print()
            print(f"  {ROJO}{NEGRITA}LA SEÑAL TE HA ENCONTRADO.{R}")
            print()
            operador.resultado = "muerte"
            operador.causa_fin = "Capturado por entidad hostil"
            break

        incidente = evento_aleatorio(prob_evento)
        if incidente:
            fn_sonido = SONIDOS_EVENTO.get(incidente["id"])
            if fn_sonido:
                fn_sonido()
            mensajes_incidente = aplicar_evento(incidente, operador)
            for linea in mensajes_incidente:
                print(linea)
                pausa(0.04)

        if not operador.esta_vivo():
            break

        direccion = pedir_direccion()
        if direccion is None:
            operador.resultado = "tiempo"
            operador.causa_fin = "Operador abandonó el turno"
            break

        dx, dy = MOVIMIENTOS[direccion]
        pos_anterior = (operador.x, operador.y)
        movio, mensaje_error = operador.mover(dx, dy, mundo)

        if not movio:
            print(f"\n{mensaje_error}")
            operador.turnos_restantes -= 1
            operador.turnos_superados += 1
        else:
            print(f"\n  Movimiento: {direccion.upper()}"
                  f"  |  ({pos_anterior[0]},{pos_anterior[1]}) → ({operador.x},{operador.y})")

        pausa(0.1)

    if operador.resultado is None:
        if operador.lucidez <= 0:
            operador.causa_fin = "Lucidez agotada — colapso del operador"
            operador.resultado = "locura"
            sonido.pausar_estatico()
            sonido.sonido_muerte()
        else:
            operador.causa_fin = "Tiempo operativo agotado"
            operador.resultado = "tiempo"

    mostrar_informe(operador, config_inicial, mundo.monstruo.veces_detectado)
    sonido.pausar_estatico()


def jugar():
    pantalla_inicio()
    sonido.iniciar_estatico()
    nombre_operador, nivel = configurar_turno()

    mundo = Mundo()
    operador = Operador(
        nombre=nombre_operador, x=0, y=0,
        lucidez=nivel["lucidez"],
        turnos_max=nivel["turnos"],
    )

    print("  Iniciando turno...")
    pausa(0.8)
    print()
    simular_turno(operador, mundo, nivel)


def main():
    while True:
        jugar()
        print()
        respuesta = input("  ¿Iniciar nuevo turno? (s/n): ").strip().lower()
        if respuesta not in ("s", "si", "sí", "y", "yes"):
            print()
            print("  Cerrando sesión.")
            print()
            sys.exit(0)
        print()


if __name__ == "__main__":
    main()