import pyglet
import random
from constants import *

window = pyglet.window.Window(caption = "Zabudataja",
                              width = 1500,
                              height = 1000)

house = pyglet.image.load("house.png")
house.anchor_x = house.width // 2
house.anchor_y = house.height // 2
sprite = pyglet.sprite.Sprite(house)
sprite.x = width // 2
sprite.y = height // 2
sprite.rotation = 23

hedhehogs  = []
imag = pyglet.image.load("grafics/jezko.png")
imag.anchor_x = imag.width // 2
imag.anchor_y = imag.height // 2

batch = pyglet.graphics.Batch()


for i in range(0, 30):
    hedhehogs.append(pyglet.sprite.Sprite(imag, batch = batch))
    hedhehogs[-1].x = random.randint(0, width)
    hedhehogs[-1].y = random.randint(0, height)

D = {pyglet.window.key.DOWN : (0, -1),
     pyglet.window.key.UP : (0, 1),
     pyglet.window.key.LEFT : (-1, 0),
     pyglet.window.key.RIGHT : (1, 0)}

pressed = {pyglet.window.key.DOWN : False,
           pyglet.window.key.UP : False,
           pyglet.window.key.LEFT : False,
           pyglet.window.key.RIGHT : False}

texts = []

@window.event
def on_key_press(symbol, modifiers):
    if symbol in D:
        pressed[symbol] = True

@window.event
def on_key_release(symbol, modifiers):
    if symbol in D:
        pressed[symbol] = False

@window.event
def on_mouse_press(x, y, button, modifiers):
    print("Mysku si stlacil na poz " + str(x) + " ; " + str(y) + " tlacidlom " + str(button))

@window.event
def on_draw():
    window.clear()
    sprite.draw()
    batch.draw()

def update(dt):
    for key, d in D.items():
        if pressed[key]:
            sprite.x += d[0] * dt * 40
            sprite.y += d[1] * dt * 40
    for nunu in hedhehogs:
        nunu.x += random.randint(-5, 5)
        nunu.y += random.randint(-5, 5)
        if nunu.x < 0:
            nunu.x = 0
        if nunu.x > width:
            nunu.x = width
        if nunu.y > height:
            nunu.y = height
        if nunu.y < 0:
            nunu.y = 0
        if abs(nunu.x - sprite.x) < sprite.width and abs(nunu.y - sprite.y) < sprite.height:
            texts.append(pyglet.text.Label('Jezkove oci!',
                                           font_name = 'Times New Roman',
                                           font_size = 36,
                                           x = random.randint(0, width), y = random.randint(0, height),
                                           batch = batch))
            nunu.x = random.randint(0, width)
            nunu.y = random.randint(0, height)
    

pyglet.clock.schedule_interval(update, 1.00000 / FPS)

pyglet.app.run()
