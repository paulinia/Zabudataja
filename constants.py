import pyglet
import os

FPS = 60
STEP = 1 / 50
height = 768
width = 1408

D = {pyglet.window.key.S : (0, -1),
     pyglet.window.key.W : (0, 1),
     pyglet.window.key.A : (-1, 0),
     pyglet.window.key.D : (1, 0)}

pressed = {pyglet.window.key.W : False,
           pyglet.window.key.S : False,
           pyglet.window.key.A : False,
           pyglet.window.key.D : False,
           pyglet.window.key.ENTER : False}

used = {}

symbols = [pyglet.window.key.W,
           pyglet.window.key.D,
           pyglet.window.key.S,
           pyglet.window.key.A]

size = 64

audio_effects = {"DEAD": pyglet.resource.media(os.path.join('sounds', 'Dying Soul.aiff'), streaming = False)}
audio_levels = {"11":    pyglet.resource.media(os.path.join("sounds", "bensound-extremeaction.wav"), streaming = False),
                "TEXT":  pyglet.resource.media(os.path.join("sounds", "bensound-sadday.wav"), streaming = False),
                "1":     pyglet.resource.media(os.path.join("sounds", "Chimera.wav"), streaming = False),
                "2":     pyglet.resource.media(os.path.join("sounds", "Palpitations.wav"), streaming = False),
                "3":     pyglet.resource.media(os.path.join("sounds", "Creepy Hollow.wav"), streaming = False),
                "4":     pyglet.resource.media(os.path.join("sounds", "Grinding Wheel.wav"), streaming = False),
                "5":     pyglet.resource.media(os.path.join("sounds", "bensound-instinct.wav"), streaming = False),
                "6":     pyglet.resource.media(os.path.join("sounds", "Last Stand.wav"), streaming = False),
                "7":     pyglet.resource.media(os.path.join("sounds", "Evil Around.wav"), streaming = False),
                "8":     pyglet.resource.media(os.path.join("sounds", "Necropolis.wav"), streaming = False),
                "9":     pyglet.resource.media(os.path.join("sounds", "Decline And Fall.wav"), streaming = False),
                "10":    pyglet.resource.media(os.path.join("sounds", "Last Stand.wav"), streaming = False),
                "12":    pyglet.resource.media(os.path.join("sounds", "bensound-ofeliasdream.wav"), streaming = False),
                "13":    pyglet.resource.media(os.path.join("sounds", "End Of Days.wav"), streaming = False),
                "OPEN":  pyglet.resource.media(os.path.join("sounds", "Sqeaking_door.wav"), streaming = False)}

loops_levels = {key : pyglet.media.SourceGroup(item.audio_format, None) for key, item in audio_levels.items()}

for key, audio in audio_levels.items():
    loops_levels[key].loop = True
    loops_levels[key].queue(audio)
