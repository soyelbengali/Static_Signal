# SEÑAL ESTÁTICA

> Turno de noche. Frecuencia 156.8 MHz. Tú eres el único que escucha.

Eres un operador de radio de emergencias en un turno de noche que empieza a comportarse de forma extraña. Algo se mueve ahí fuera. Sobrevive hasta el amanecer.

---

## Requisitos

- Python 3.11 o superior
- Sin dependencias externas — solo biblioteca estándar de Python
- Los sonidos funcionan únicamente en **Windows** (winsound). En Mac/Linux el juego funciona igual pero sin audio.

---

## Cómo ejecutar

```bash
python main.py
```

Coloca los archivos de sonido `staticshort.wav` y `heartbeatshort.wav` en la misma carpeta que `main.py`.

---

## Archivos del proyecto

```
main.py       — Bucle principal y lógica del juego
mundo.py      — Mapa, sectores, monstruo y sus efectos
operador.py   — Clase del personaje jugador
eventos.py    — Eventos aleatorios
mapa.py       — Radar visual y brújula en terminal
informe.py    — Informe final de la expedición
sonido.py     — Módulo de sonidos (winsound, solo Windows)
README.md     — Este archivo
```

---

## Cómo se juega

1. Introduce tu nombre y elige dificultad.
2. Cada turno muestra el radar, tu posición, lucidez y hora.
3. Elige dirección para moverte: `n`, `s`, `e`, `o`, `ne`, `no`, `se`, `so`
4. Sobrevive todos los turnos sin perder la lucidez ni ser atrapado.

---

## Condiciones de fin

| Condición | Resultado |
|---|---|
| Sobrevives todos los turnos | Victoria |
| Lucidez llega a 0 | Derrota — colapso |
| El monstruo te alcanza | Derrota — capturado |
| Escribes `salir` | Abandono |

---

## Sectores del mapa

| Símbolo | Tipo | Efecto |
|---|---|---|
| `[◉]` | Tú | — |
| `[X]` | Señal (monstruo) | Solo visible en persecución |
| `[L]` | Llamada | Lucidez −5 a −15 |
| `[S]` | Silencio | Lucidez −1 a −8 |
| `[I]` | Interferencia | Lucidez −10 a −20, puede atraer al monstruo |
| `[R]` | Refugio | Lucidez +8 a +20, dura 3 usos |
| `[?]` | Anomalía | Lucidez −15 a −25, te teleporta |
| `[C]` | Café | Lucidez +5 a +12, dura 2 usos |
| `[D]` | Diario | Lucidez +8 a +15, dura 1 uso |
| `[~]` | Radio vieja | Lucidez +6 a +14, dura 2 usos |
| `[F]` | Foto | Lucidez +10 a +18, dura 1 uso |
| ` · ` | Sin explorar | — |
| ` ○ ` | Borde del radar | — |

---

## La señal — comportamiento del monstruo

El monstruo tiene tres fases:

- **Patrulla** `[x]` gris — se mueve al azar, no sabe dónde estás. Invisible en el radar.
- **Persecución** `[X]` rojo — viene directo hacia ti. Visible en el radar. La brújula apunta hacia él.
- **Retirada** `[~]` amarillo — huye hacia el borde del mapa. No puede matarte. Invisible en el radar.

Se activa la persecución si:
- Te acercas a 4 pasos o menos (distancia Manhattan)
- Pisas un sector `[L]` llamada (35% de prob.) o `[I]` interferencia (55% de prob.)

La persecución dura entre 4 y 12 turnos aleatorios. Al terminar, el monstruo se retira y reaparece por un borde aleatorio del mapa.

---

## Mecánicas especiales

- **Hora del turno** — la hora avanza 7 minutos por turno. Empieza a las 23:00.
- **Textos rotos** — por debajo del 20% de lucidez los mensajes se vuelven fragmentados y extraños.
- **Sectores que se agotan** — refugio, café, diario, radio y foto tienen un número limitado de usos. Una vez agotados se convierten en sector vacío.
- **Brújula** — siempre apunta hacia el monstruo. Solo muestra distancia y coordenadas exactas durante la persecución.

---

## Dificultades

| Nivel | Lucidez | Turnos | Prob. evento |
|---|---|---|---|
| Fácil | 100 | 20 | 20% |
| Normal | 80 | 30 | 35% |
| Difícil | 60 | 40 | 50% |