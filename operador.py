class Operador:
    def __init__(self, nombre, x, y, lucidez, pasos_max):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.lucidez = lucidez
        self.lucidez_max = lucidez
        self.turnos_restantes = pasos_max
        self.turnos_superados = 0
        self.eventos_ocurridos = []
        self.sectores_visitados = []
        self.causa_fin = None
        self.resultado = None
        self._hora = 23 * 60

    def hora_actual(self):
        total = self._hora % (24 * 60)
        h = total // 60
        m = total % 60
        return f"{h:02d}:{m:02d}"

    def avanzar_hora(self, minutos=7):
        self._hora += minutos

    def mover(self, dx, dy, mundo):
        nx = self.x + dx
        ny = self.y + dy
        if not mundo.dentro_de_limites(nx, ny):
            return False,
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
            return "ESTABLE"
        elif pct > 0.50:
            return "ALERTA"
        elif pct > 0.25:
            return "CRÍTICO"
        else:
            return "⚠ COLAPSO INMINENTE"

    def textos_rotos(self):
        return self.lucidez / self.lucidez_max < 0.20