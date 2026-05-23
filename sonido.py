import time

try:
    import winsound
    _SONIDO = True
except ImportError:
    _SONIDO = False


# utilidades internas 

def _beep(freq, dur):
    if _SONIDO:
        try:
            winsound.Beep(freq, dur)
        except Exception:
            pass

def _play(archivo, flags=0):
    if _SONIDO:
        try:
            winsound.PlaySound(archivo, flags)
        except Exception:
            pass


# fondo estático 

def iniciar_estatico():
    """Reproduce staticshort.wav en bucle de fondo."""
    if _SONIDO:
        _play("staticshort.wav",
              winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

def pausar_estatico():
    """Para el estático de fondo (silencio total)."""
    if _SONIDO:
        _play(None, winsound.SND_PURGE)

def reanudar_estatico():
    """Reanuda el estático tras un silencio."""
    iniciar_estatico()


# eventos 

def sonido_llamada_propia():
    """Latido doble — lub dub, lub dub."""
    for _ in range(2):
        _play("heartbeatshort.wav", winsound.SND_FILENAME)
        time.sleep(0.18)
        _play("heartbeatshort.wav", winsound.SND_FILENAME)
        time.sleep(0.55)                                    

def sonido_grabacion():
    """Tono grave — grabación anómala."""
    _beep(300, 700)

def sonido_transmision_fragmentada():
    """Interferencia de frecuencias — transmisión fragmentada."""
    _beep(1000, 60)
    _beep(200,  120)
    _beep(900,  60)

def sonido_coordenadas_imposibles():
    """Pitido agudo seguido de tono bajo — error de sistema."""
    _beep(1200, 80)
    _beep(400,  300)

def sonido_unidad_perdida():
    """Tono sostenido — señal que se apaga."""
    _beep(500, 500)

def sonido_voz_repetida():
    """Dos tonos iguales separados — eco de llamada."""
    _beep(660, 150)
    time.sleep(0.08)
    _beep(660, 150)

def sonido_numero_propio():
    """Tono ascendente perturbador."""
    for freq in [400, 500, 650, 800]:
        _beep(freq, 80)

def sonido_momento_claridad():
    """Acorde breve — lucidez repentina."""
    _beep(880, 100)
    _beep(1100, 80)

def sonido_señal_limpia():
    """Silencio — el estático desaparece y vuelve."""
    pausar_estatico()
    time.sleep(1.2)
    reanudar_estatico()

def sonido_deteccion():
    """Alarma de detección — el monstruo te ha visto."""
    _beep(900, 120)
    _beep(700, 120)
    _beep(900, 200)

def sonido_muerte():
    """Tono descendente de fin."""
    for freq in [600, 450, 300, 180]:
        _beep(freq, 180)

def sonido_victoria():
    """Acorde ascendente de victoria."""
    for freq in [440, 550, 660, 880]:
        _beep(freq, 120)


# sector

def sonido_sector(tipo):
    """Sonido ambiental al entrar en un sector."""
    if tipo == "silencio":
        pausar_estatico()
        time.sleep(0.8)
        reanudar_estatico()
    elif tipo == "interferencia":
        _beep(150, 200)
        _beep(80,  150)
    elif tipo == "anomalia":
        _beep(1400, 60)
        _beep(200,  200)
        _beep(1100, 60)
    elif tipo == "refugio":
        _beep(740, 120)
    elif tipo == "llamada":
        _beep(480, 200)
        time.sleep(0.1)
        _beep(480, 100)
