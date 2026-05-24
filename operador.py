class Operador:
    def __init__(self, nombre, x, y, lucidez, turnos_max):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.lucidez = lucidez
        self.lucidez_max = lucidez
        self.turnos_restantes = turnos_max
        self.turnos_superados = 0
        self.eventos_ocurridos = []
        self.sectores_visitados = []
        self.causa_fin = None
        self.resultado = None
        self._minutos = 23 * 60

    def hora_actual(self):
        total = self._minutos % (24 * 60)
        return f"{total // 60:02d}:{total % 60:02d}"

    def avanzar_hora(self, minutos=7):
        self._minutos += minutos

    def mover(self, dx, dy, mundo):
        nx = self.x + dx
        ny = self.y + dy
        if not mundo.dentro_de_limites(nx, ny):
            return False, "  >> Out of coverage. You cannot go beyond the operational limits."
        self.x = nx
        self.y = ny
        self.turnos_restantes -= 1
        self.turnos_superados += 1
        return True, None

    def esta_vivo(self):
        return self.lucidez > 0 and self.turnos_restantes > 0

    def estado_lucidez(self):
        pct = self.lucidez / self.lucidez_max
        if pct > 0.75:
            return "STABLE"
        elif pct > 0.50:
            return "ALERT"
        elif pct > 0.25:
            return "CRITICAL"
        return "⚠ IMMINENT COLLAPSE"

    def alucinando(self):
        return self.lucidez / self.lucidez_max < 0.20
