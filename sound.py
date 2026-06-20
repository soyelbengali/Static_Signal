import time

try:
    import winsound
    _SOUND_ENABLED = True
except ImportError:
    _SOUND_ENABLED = False


# internal helpers

def _beep(freq, dur):
    if _SOUND_ENABLED:
        try:
            winsound.Beep(freq, dur)
        except Exception:
            pass

def _play(file, flags=0):
    if _SOUND_ENABLED:
        try:
            winsound.PlaySound(file, flags)
        except Exception:
            pass


# background static

def start_static():
    """Plays staticshort.wav as a looping background track."""
    if _SOUND_ENABLED:
        _play("staticshort.wav",
              winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

def pause_static():
    """Stops the background static (total silence)."""
    if _SOUND_ENABLED:
        _play(None, winsound.SND_PURGE)

def resume_static():
    """Resumes the static after a silence."""
    start_static()


# events

def sound_own_call():
    """Double heartbeat — lub dub, lub dub."""
    for _ in range(2):
        _play("heartbeatshort.wav", winsound.SND_FILENAME)
        time.sleep(0.18)
        _play("heartbeatshort.wav", winsound.SND_FILENAME)
        time.sleep(0.55)

def sound_recording():
    """Low tone — anomalous recording."""
    _beep(300, 700)

def sound_fragmented_transmission():
    """Frequency interference — fragmented transmission."""
    _beep(1000, 60)
    _beep(200,  120)
    _beep(900,  60)

def sound_impossible_coordinates():
    """Sharp beep followed by a low tone — system error."""
    _beep(1200, 80)
    _beep(400,  300)

def sound_lost_unit():
    """Sustained tone — signal fading out."""
    _beep(500, 500)

def sound_repeated_voice():
    """Two identical tones, spaced apart — call echo."""
    _beep(660, 150)
    time.sleep(0.08)
    _beep(660, 150)

def sound_own_number():
    """Unsettling ascending tone."""
    for freq in [400, 500, 650, 800]:
        _beep(freq, 80)

def sound_moment_of_clarity():
    """Brief chord — sudden clarity."""
    _beep(880, 100)
    _beep(1100, 80)

def sound_clean_signal():
    """Silence — the static fades out and returns."""
    pause_static()
    time.sleep(1.2)
    resume_static()

def sound_detection():
    """Detection alarm — the monster has seen you."""
    _beep(900, 120)
    _beep(700, 120)
    _beep(900, 200)

def sound_death():
    """Descending tone marking the end."""
    for freq in [600, 450, 300, 180]:
        _beep(freq, 180)

def sound_victory():
    """Ascending victory chord."""
    for freq in [440, 550, 660, 880]:
        _beep(freq, 120)


# sector

def sound_sector(sector_type):
    """Ambient sound when entering a sector."""
    if sector_type == "silence":
        pause_static()
        time.sleep(0.8)
        resume_static()
    elif sector_type == "interference":
        _beep(150, 200)
        _beep(80,  150)
    elif sector_type == "anomaly":
        _beep(1400, 60)
        _beep(200,  200)
        _beep(1100, 60)
    elif sector_type == "shelter":
        _beep(740, 120)
    elif sector_type == "call":
        _beep(480, 200)
        time.sleep(0.1)
        _beep(480, 100)
