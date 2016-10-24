from constants import *
import utility
import os
import sys
import editor
import camera

window = pyglet.window.Window(caption = "Editor",
                              width = width,
                              height = height)
    
camera_map = camera.Camera(width, height, (0, 0), 1)
camera_real = camera.Camera(width, height, (width / 2, height / 2), 1)
curent = None

cx, cy = 0, 0

@window.event
def on_key_press(symbol, modifiers):
    global curent, keys, level
    used[symbol] = False
    pressed[symbol] = True
    if symbol in keys:
        curent = keys[symbol]
        level.key_press(curent)

@window.event
def on_key_release(symbol, modifiers):
    pressed[symbol] = False
    used[symbol] = False

@window.event
def on_mouse_press(x, y, button, modifiers):
    global curent
    if button == pyglet.window.mouse.RIGHT:
       curent = None
    elif button == pyglet.window.mouse.LEFT and curent != None:
        game_x, game_y = utility.conventer(camera_map.zoom, cx, cy, x, y)
        level.add_entity(curent, game_x // size, game_y // size)

@window.event
def on_draw():
    global texts
    window.clear()
    camera_map.begin()
    level.draw()
    camera_map.end()
    
    camera_real.begin()
    texts[curent].draw()
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (utility.mouse_x, utility.mouse_y,
                                                             utility.mouse_x - 6, utility.mouse_y - 12,
                                                             utility.mouse_x, utility.mouse_y - 6,
                                                             utility.mouse_x + 6, utility.mouse_y - 12)), ('c3B', (255, 20, 20) * 4))
    camera_real.end()
    
@window.event
def on_mouse_motion(x, y, dx, dy):
    utility.mouse_x = x
    utility.mouse_y = y

def update(dt):
    global cx, cy
    camera_map.position = (cx, cy)
    if pyglet.window.key.EQUAL in pressed and pressed[pyglet.window.key.EQUAL]:
        camera_map.zoom *= (dt + 1)
    if pyglet.window.key.MINUS in pressed and pressed[pyglet.window.key.MINUS]:
        camera_map.zoom /= (dt + 1)
    if pyglet.window.key.UP in pressed and pressed[pyglet.window.key.UP]:
        cy += (500 / camera_map.zoom) * dt
    if pyglet.window.key.DOWN in pressed and pressed[pyglet.window.key.DOWN]:
        cy -= (500 / camera_map.zoom) * dt
    if pyglet.window.key.RIGHT in pressed and pressed[pyglet.window.key.RIGHT]:
        cx += (500 / camera_map.zoom) * dt
    if pyglet.window.key.LEFT in pressed and pressed[pyglet.window.key.LEFT]:
        cx -= (500 / camera_map.zoom) * dt

level = editor.Level()
window.set_mouse_visible(False)

@window.event
def on_close():
    global level
    level.write_to_file()

if sys.argv[1] == 'load' or sys.argv[1] == 'open':
    level.load_level(sys.argv[2])
else:
    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])
    level.create_level(sys.argv[2])

texts = {
    None : pyglet.text.Label("E : enemy, Q : item, F : player, S : spell, W : Wall, D : Demolish, R : Grandma", font_name = 'Times New Roman', 
                               font_size = 20, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 100),
    "ENEMY" : pyglet.text.Label("Creating enemy", font_name = 'Times New Roman', font_size = 20, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 100),
    "PLAYER" : pyglet.text.Label("Creating player", font_name = 'Times New Roman', font_size = 20, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 100),
    "SPELL" : pyglet.text.Label("Creating spell", font_name = 'Times New Roman', font_size = 20, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 100),
    "ITEM" : pyglet.text.Label("Creating item", font_name = 'Times New Roman', font_size = 20, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 100),
    "WALL" : pyglet.text.Label("Creating wall", font_name = 'Times New Roman', font_size = 20, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 100),
    "GRANDMA" : pyglet.text.Label("Creating grandma", font_name = 'Times New Roman', font_size = 20, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 100),
    "DEMOLISH" : pyglet.text.Label("Demolishing wall", font_name = 'Times New Roman', font_size = 20, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 100)
    }

keys = {
    pyglet.window.key.E : "ENEMY",
    pyglet.window.key.Q : "ITEM",
    pyglet.window.key.F : "PLAYER",
    pyglet.window.key.S : "SPELL",
    pyglet.window.key.W : "WALL",
    pyglet.window.key.D : "DEMOLISH",
    pyglet.window.key.R : "GRANDMA"
    }

pyglet.clock.schedule_interval(update, 1 / FPS)

pyglet.app.run()
