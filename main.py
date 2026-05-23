import random
import time
import sys

from mundo import Mundo, LIMITE_MIN, LIMITE_MAX, texto_roto_sector
from operador import Operador
from eventos import evento_aleatorio, aplicar_evento
from informe import mostrar_informe, LINEA, pausar
from mapa import dibujar_mapa, ROJO, NEGRITA, AMARILLO, GRIS, R
import sonido

DIRECCIONES = {
    "n":  ( 0,  1), "s":  ( 0, -1),
    "e":  ( 1,  0), "o":  (-1,  0),
    "ne": ( 1,  1), "no": (-1,  1),
    "se": ( 1, -1), "so": (-1, -1),
}

ALIAS = {
    "norte": "n", "arriba": "n",
    "sur":   "s", "abajo":  "s",
    "este":  "e", "derecha":"e",
    "oeste": "o", "izquierda":"o",
}

DIFICULTADES = {
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


def pedir_entero(mensaje, minimo, maximo, defecto=None):
    while True:
        entrada = input(mensaje).strip()
        if entrada == "" and defecto is not None:
            return defecto
        try:
            valor = int(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f"  Introduce un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  Valor no válido. Introduce un número entero.")


def pedir_texto(mensaje, defecto="Operador"):
    entrada = input(mensaje).strip()
    return entrada if entrada else defecto


def mostrar_bienvenida():
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


def pedir_parametros():
    print("  CONFIGURACIÓN DEL TURNO")
    print()
    nombre = pedir_texto("  Nombre del operador (Enter = 'Operador'): ")
    print()
    print("  Dificultad:")
    for k, v in DIFICULTADES.items():
        print(f"    {k}. {v['nombre']:8} — lucidez {v['lucidez']}, turnos {v['turnos']}")
    dif_key = input("  Elige (1/2/3, Enter = 2): ").strip()
    if dif_key not in DIFICULTADES:
        dif_key = "2"
    dif = DIFICULTADES[dif_key]
    print()
    print(LINEA)
    print()
    print(f"  Operador       : {nombre}")
    print(f"  Posición inicio: X=0, Y=0")
    print(f"  Lucidez        : {dif['lucidez']}")
    print(f"  Turnos objetivo: {dif['turnos']}")
    print(f"  Dificultad     : {dif['nombre']}")
    print()
    print(f"  Límites: X=[{LIMITE_MIN},{LIMITE_MAX}]  Y=[{LIMITE_MIN},{LIMITE_MAX}]")
    print("  Victoria : sobrevivir todos los turnos")
    print("  Derrota  : lucidez=0 / atrapado / abandonar")
    print()
    print(LINEA)
    print()
    return nombre, dif


def mostrar_estado(op, mundo, paso, turnos_total):
    print(f"\n  — TURNO {paso}/{turnos_total}   {op.hora_actual()} —")
    dibujar_mapa(op, mundo)
    print(f"  Estado lucidez   : [{op.estado_lucidez()}]")
    print(f"  Turnos restantes : {op.turnos_restantes}")


def pedir_direccion():
    print()
    print("  Direcciones: n / s / e / o / ne / no / se / so")
    print("  ('salir' para abandonar el turno)")
    while True:
        entrada = input("  > ").strip().lower()
        if entrada == "salir":
            return None
        entrada = ALIAS.get(entrada, entrada)
        if entrada in DIRECCIONES:
            return entrada
        print("  Dirección no reconocida.")


def bucle_simulacion(op, mundo, dif):
    turnos_total = dif["turnos"]
    prob_evento  = dif["prob_evento"]
    params_iniciales = {
        "x": op.x, "y": op.y,
        "lucidez": op.lucidez_max,
        "pasos": op.turnos_restantes,
    }

    paso = 0

    while op.esta_vivo():
        paso += 1

        if paso > turnos_total:
            op.resultado = "victoria"
            op.causa_fin = "Supervivencia completada"
            sonido.sonido_victoria()
            break

        mostrar_estado(op, mundo, paso, turnos_total)
        op.avanzar_hora(7)

        # sector actual
        sector_actual = mundo.obtener_sector(op.x, op.y)
        if not sector_actual.visitado:
            sector_actual.visitado = True
            op.sectores_visitados.append((op.x, op.y, sector_actual.tipo_visible()))
            sonido.sonido_sector(sector_actual.tipo)

        tipo_visible = sector_actual.tipo_visible()
        print(f"  Sector  : {tipo_visible.upper()} — {sector_actual.descripcion()}")

        # textos rotos si lucidez baja
        if op.textos_rotos():
            print(texto_roto_sector(tipo_visible))

        mensajes_sector = mundo.aplicar_efecto(sector_actual, op)
        for msg in mensajes_sector:
            print(msg)
            pausa(0.04)

        if not op.esta_vivo():
            break

        # monstruo
        m = mundo.monstruo
        fase_antes = m.fase

        detectado, motivo = m.comprobar_deteccion(op, sector_actual.tipo)
        if detectado and m.fase == "patrulla":
            m.iniciar_persecucion()
            sonido.sonido_deteccion()
            print(f"\n  {ROJO}{NEGRITA}⚠  SEÑAL DETECTADA — {motivo.upper()}{R}")
            print(f"  {ROJO}Algo viene hacia ti.{R}")
            pausa(0.2)

        m.mover(op.x, op.y)

        if m.fase != fase_antes:
            if m.fase == "retirada":
                print(f"\n  {AMARILLO}  La señal pierde tu rastro. Se aleja.{R}")
                sonido.reanudar_estatico()
            elif m.fase == "patrulla":
                print(f"\n  {GRIS}  Silencio. La señal vuelve a vagar.{R}")

        if m.colision(op.x, op.y):
            sonido.pausar_estatico()
            sonido.sonido_muerte()
            print()
            print(f"  {ROJO}{NEGRITA}LA SEÑAL TE HA ENCONTRADO.{R}")
            print()
            op.resultado = "muerte"
            op.causa_fin = "Capturado por entidad hostil"
            break

        # evento aleatorio
        ev = evento_aleatorio(prob_evento)
        if ev:
            fn_sonido = SONIDOS_EVENTO.get(ev["id"])
            if fn_sonido:
                fn_sonido()
            mensajes_ev = aplicar_evento(ev, op)
            for msg in mensajes_ev:
                print(msg)
                pausa(0.04)

        if not op.esta_vivo():
            break

        direccion = pedir_direccion()
        if direccion is None:
            op.resultado = "tiempo"
            op.causa_fin = "Operador abandonó el turno"
            break

        dx, dy = DIRECCIONES[direccion]
        pos_antes = (op.x, op.y)
        ok, msg_error = op.mover(dx, dy, mundo)

        if not ok:
            print(f"\n{msg_error}")
            op.turnos_restantes -= 1
            op.turnos_superados += 1
        else:
            print(f"\n  Movimiento: {direccion.upper()}"
                  f"  |  ({pos_antes[0]},{pos_antes[1]}) → ({op.x},{op.y})")

        pausa(0.1)

    if op.resultado is None:
        if op.lucidez <= 0:
            op.causa_fin = "Lucidez agotada — colapso del operador"
            op.resultado = "locura"
            sonido.pausar_estatico()
            sonido.sonido_muerte()
        else:
            op.causa_fin = "Tiempo operativo agotado"
            op.resultado = "tiempo"

    mostrar_informe(op, params_iniciales, mundo.monstruo.veces_detectado)
    sonido.pausar_estatico()


def jugar():
    mostrar_bienvenida()
    sonido.iniciar_estatico()
    nombre, dif = pedir_parametros()

    mundo    = Mundo()
    operador = Operador(
        nombre=nombre, x=0, y=0,
        lucidez=dif["lucidez"],
        pasos_max=dif["turnos"],
    )

    print("  Iniciando turno...")
    pausa(0.8)
    print()
    bucle_simulacion(operador, mundo, dif)


def main():
    while True:
        jugar()
        print()
        resp = input("  ¿Iniciar nuevo turno? (s/n): ").strip().lower()
        if resp not in ("s", "si", "sí", "y", "yes"):
            print()
            print("  Cerrando sesión.")
            print()
            sys.exit(0)
        print()


if __name__ == "__main__":
    main()