# SEÑAL ESTÁTICA

> Turno de noche. Frecuencia 156.8 MHz. Tú eres el único que escucha.

Simulador de texto en terminal. Eres un operador de radio de emergencias en un turno de noche que empieza a comportarse de forma extraña. Muévete por el mapa de coordenadas, gestiona tu lucidez y llega al punto de relevo antes de que todo se derrumbe.

---

## Requisitos

- Python 3.11 o superior
- Sin dependencias externas (solo biblioteca estándar)

---

## Cómo ejecutar

```bash
python main.py
```

o en sistemas donde coexisten Python 2 y 3:

```bash
python3 main.py
```

---

## Archivos del proyecto

```
main.py       — Bucle principal y lógica del juego
mundo.py      — Mapa, sectores y sus efectos
operador.py   — Clase del personaje jugador
eventos.py    — Eventos aleatorios
informe.py    — Informe final de la expedición
README.md     — Este archivo
```

---

## Cómo se juega

1. Introduce el nombre del operador y los parámetros iniciales.
2. Cada turno muestra tu posición, lucidez y pasos restantes.
3. Elige dirección: `n`, `s`, `e`, `o`, `ne`, `no`, `se`, `so`
4. Llega al punto de relevo (coordenadas objetivo) antes de quedarte sin lucidez o sin pasos.

### Condiciones de fin

| Condición | Resultado |
|---|---|
| Llegas al punto de relevo | Victoria |
| Lucidez llega a 0 | Derrota — colapso |
| Pasos agotados | Derrota — tiempo |
| Escribes `salir` | Abandono |

---

## Elementos del mundo

| Sector | Efecto |
|---|---|
| Vacío | Sin efecto |
| Llamada | Lucidez −5 a −15 |
| Silencio | Lucidez −5 a −10 |
| Interferencia | Lucidez −10 a −20 |
| Refugio | Lucidez +8 a +15 |
| Anomalía | Lucidez −15 a −25, posición aleatoria |
| Amanecer | Victoria |
