from constants import *
import levels
import utility
import camera
from pyglet.gl import *

window = pyglet.window.Window(caption = "Zabudataja",
                              width = width,
                              height = height)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
window.set_mouse_visible(False)

class GameState:
    def __init__(self):
        self.player = pyglet.media.Player()
        with open("last", 'r') as last:
            for line in last:
                self.id_level = int(line)
        self.level = None
        self.max_level = 13
        self.middle = pyglet.sprite.Sprite(pyglet.resource.image(os.path.join("graphics", "middle.png")), x = width // 2, y =  height // 2)
        self.stones = pyglet.sprite.Sprite(pyglet.resource.image(os.path.join("graphics", "stones.png")), x = width // 2, y =  height // 2)
        self.mode = "TEXT"
        self.player.queue(loops_levels["TEXT"])
        self.state = 0
        self.camera = camera.Camera(width, height, (width / 2, height / 2), 1)
        text = self.get_text()
        self.intro_texts = [[pyglet.text.Label(line, font_name = 'Times New Roman', font_size = 30, anchor_x = 'center', anchor_y = 'center',
                                               x = width // 2, y = height - 60 - i * size) for i, line in enumerate(replica)] for replica in text]
        
    def draw(self):
        if self.mode == 'GAME':
            self.level.draw()
        elif self.mode == 'OPEN':
            self.camera.begin()
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (0, 0, width, 0,
                                                                 width, height, 0, height)), ('c3B', (100, 0, 100) * 4))
            
            self.middle.scale = (5 - self.state * 0.01)
            self.middle.position = (width // 2 - self.middle.width // 2, height // 2 - self.middle.height // 2)
            self.stones.scale = (4.9 + self.state * 0.01)
            self.stones.position = (width // 2 - self.stones.width // 2, height // 2 - self.stones.height // 2)
            self.middle.draw()
            self.stones.draw()
            
            self.camera.end()
        elif self.mode == 'TEXT':
            self.camera.begin()
            for text in self.intro_texts[self.state]:
                text.draw()
            self.camera.end()
    
    def get_text(self):
        tfile = open(os.path.join("levels", str(self.id_level), "text"), 'r')
        lines = [line[:-1] for line in tfile.readlines()]
        return [utility.split(30, message) for message in lines]
    
    def update(self, dt):
        if pyglet.window.key.ESCAPE in pressed and pressed[pyglet.window.key.ESCAPE]:
            self.player.pause()
            return 'MENU'
        if self.mode == 'GAME':
            res = self.level.update(dt)
            if res == 'EXIT':
                self.next_level()
            if res == 'SACR':
                self.player.pause()
                return "ENDG"
            if res == "LOST":
                self.player.pause()
                return "LOST"
            if res == 'REPL':
                self.player.seek(0)
        elif self.mode == 'OPEN':
            self.state += 1
            if self.state == 500:
                self.state = 0
                self.player.queue(loops_levels["TEXT"])
                self.player.next_source()
                self.mode = 'TEXT'
                text = self.get_text()
                self.intro_texts = [[pyglet.text.Label(line, font_name = 'Times New Roman', font_size = 30, anchor_x = 'center', anchor_y = 'center',
                                                    x = width // 2, y = height - 60 - i * size) for i, line in enumerate(replica)] for replica in text]
                
        return "GAME"
    
    def next_level(self):
        if self.id_level > self.max_level:
            self.end_game()
        self.mode = 'OPEN'
        self.player.queue(loops_levels["OPEN"])
        self.player.next_source()
        self.state = 0
        self.level = levels.Level(str(self.id_level))
    
    def process_event_mouse(self, x, y, button):
        if self.mode == 'GAME':
            self.level.click(x, y, button)
        elif self.mode == 'TEXT':
            self.state += 1
            if self.state >= len(self.intro_texts):
                self.mode = 'GAME'
                self.id_level += 1
                self.player.queue(loops_levels[str(self.id_level)])
                self.player.next_source()
                self.level = levels.Level(str(self.id_level))
                self.state = 0
        return "GAME"
    
    def reload_game(self):
        self.id_level = 0
        self.mode = 'TEXT'
        self.player.queue(loops_levels["TEXT"])
        self.player.next_source()
        text = self.get_text()
        self.intro_texts = [[pyglet.text.Label(line, font_name = 'Times New Roman', font_size = 30, anchor_x = 'center', anchor_y = 'center',
                                               x = width // 2, y = height - 60 - i * size) for i, line in enumerate(replica)] for replica in text]
        self.state = 0
        
    
    def reload_level(self):
        if self.id_level > 0:
            self.level.replay()
            self.player.seek(0)
    
class EndState:
    def __init__(self):
        self.player = pyglet.media.Player()
        self.audio = pyglet.resource.media(os.path.join("sounds", "bensound-newdawn.wav"), streaming = False)
        self.looper = pyglet.media.SourceGroup(self.audio.audio_format, None)
        self.looper.loop = True
        self.looper.queue(self.audio)
        self.player.queue(self.looper)
        self.step = 255
        self.speed = 255 / 5
        self.texts = [pyglet.text.Label("Sestevelína povstala, už nie je viac Zabudatajou", font_name = 'Times New Roman', font_size = 30,
                                        anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 120, color = (0, 0, 0, 255)),
                      pyglet.text.Label("Zas zavládlo svetlo cez deň, tma v noci", font_name = 'Times New Roman', font_size = 30,
                                        anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 240, color = (0, 0, 0, 255)),
                      pyglet.text.Label("A ty? Svetlo videlo tvoju púť, Svetlo videlo", font_name = 'Times New Roman', font_size = 30,
                                        anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 360, color = (0, 0, 0, 255)),
                      pyglet.text.Label("Ako mesiac svietiš na cestu pútnikov v noci", font_name = 'Times New Roman', font_size = 30,
                                        anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 500, color = (0, 0, 0, 255)),
                      pyglet.text.Label("Klikni na skončenie hry", font_name = 'Times New Roman', font_size = 20,
                                        anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 700, color = (0, 0, 0, 255))]
        self.camera = camera.Camera(width, height, (width / 2, height / 2), 1)
        
        
    def draw(self):
        self.camera.begin()
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (0, 0, width, 0, width, height, 0, height)), ('c3B', (255, 255, 255) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (0, 0, width, 0, width, height, 0, height)), ('c4B', (0, 0, 0, max(0, int(self.step)) ) * 4))
        if self.step < 0:
            for text in self.texts:
                text.draw()
        self.camera.end()
    
    def update(self, dt):
        self.step -= dt * self.speed
        return "ENDG"
    
    def process_event_mouse(self, x, y, button):
        if self.step < 0:
            pyglet.app.exit()
        return "ENDG"
    
class LostState:
    def __init__(self):
        self.player = pyglet.media.Player()
        self.audio = pyglet.resource.media(os.path.join("sounds", "bensound-memories.wav"), streaming = False)
        self.looper = pyglet.media.SourceGroup(self.audio.audio_format, None)
        self.looper.loop = True
        self.looper.queue(self.audio)
        self.player.queue(self.looper)
        self.step = 255
        self.speed = 255 / 5
        self.texts = [pyglet.text.Label("Sestevel! Mŕtva duša vypustila svoj posledný výkrik", font_name = 'Times New Roman', font_size = 30,
                                        anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 120, color = (150, 0, 0, 255)),
                      pyglet.text.Label("A svetlo vidí svoju dcéru zhynúť - už naveky, už niet cesty späť", font_name = 'Times New Roman', font_size = 30,
                                        anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 240, color = (150, 0, 0, 255)),
                      pyglet.text.Label("Hrdina? Nad dcéry svetla mŕtvlou stojíš, kto sa ti odvďačí?", font_name = 'Times New Roman', font_size = 30,
                                        anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 360, color = (150, 0, 0, 255)),
                      pyglet.text.Label("Za smrť smrť - či si myslel's že to svetlo vráti?", font_name = 'Times New Roman', font_size = 30,
                                        anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 480, color = (150, 0, 0, 255)),
                      pyglet.text.Label("Len svetlo plače a Tma stojí - či toto chcela?", font_name = 'Times New Roman', font_size = 30,
                                        anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 600, color = (150, 0, 0, 255)),
                      pyglet.text.Label("Klikni na skončenie hry", font_name = 'Times New Roman', font_size = 20,
                                        anchor_x = 'center', anchor_y = 'center', x = width // 2, y = height - 700, color = (150, 0, 0, 255))]
        self.camera = camera.Camera(width, height, (width / 2, height / 2), 1)
        
        
    def draw(self):
        self.camera.begin()
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (0, 0, width, 0, width, height, 0, height)), ('c3B', (255, 255, 255) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (0, 0, width, 0, width, height, 0, height)), ('c4B', (0, 0, 0, min(255, 255 - int(self.step)) ) * 4))
        if self.step < 0:
            for text in self.texts:
                text.draw()
        self.camera.end()
    
    def update(self, dt):
        self.step -= dt * self.speed
        return "LOST"
    
    def process_event_mouse(self, x, y, button):
        if self.step < 0:
            pyglet.app.exit()
        return "LOST"

class MenuState:
    def __init__(self):
        self.player = pyglet.media.Player()
        self.audio = pyglet.resource.media(os.path.join("sounds", "bensound-tomorrow.wav"), streaming = False)
        self.looper = pyglet.media.SourceGroup(self.audio.audio_format, None)
        self.looper.loop = True
        self.looper.queue(self.audio)
        self.player.queue(self.looper)
        self.size = 4
        self.options = [self.end_game, self.replay_level, self.resume_game, self.start_game]
        self.pointer = 3
        self.texts = [pyglet.text.Label("End Game", font_name = 'Times New Roman', font_size = 40, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = 140),
                      pyglet.text.Label("Replay Level", font_name = 'Times New Roman', font_size = 40, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = 280),
                      pyglet.text.Label("Resume Game", font_name = 'Times New Roman', font_size = 40, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = 420),
                      pyglet.text.Label("New Game", font_name = 'Times New Roman', font_size = 40, anchor_x = 'center', anchor_y = 'center', x = width // 2, y = 560)]
        self.camera = camera.Camera(width, height, (width / 2, height / 2), 1)
        
    def draw(self):
        self.camera.begin()
        
        for text in self.texts:
            text.draw()
        
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (width // 2 - 170, self.pointer * 140 + 80,
                                                             width // 2 + 170, self.pointer * 140 + 80,
                                                             width // 2 + 170, self.pointer * 140 + 180,
                                                             width // 2 - 170, self.pointer * 140 + 180)), ('c4B', (0, 255, 0, 150) * 4))
        self.camera.end()
    
    def update(self, dt):
        for symbol in pressed:
            if pressed[symbol] and (not used[symbol]):
                used[symbol] = True
                if symbol == pyglet.window.key.UP:
                    self.pointer = min(3, self.pointer + 1)
                if symbol == pyglet.window.key.DOWN:
                    self.pointer = max(0, self.pointer - 1)
                if symbol == pyglet.window.key.SPACE or symbol == pyglet.window.key.ENTER:
                    return self.options[self.pointer]()
        255
        return "MENU"
    
    def process_event_mouse(self, x, y, button):
        return "MENU"
    
    def end_game(self):
        self.player.pause()
        global states
        with open("last", 'w') as last:
            last.write(str(max(0, states["GAME"].id_level - 1)))
        pyglet.app.exit()
        return 'MENU'
    
    def start_game(self):
        states['GAME'].reload_game()
        self.player.pause()
        return "GAME"
    
    def resume_game(self):
        self.player.pause()
        return 'GAME'
    
    def replay_level(self):
        self.player.pause()
        states['GAME'].reload_level()
        return 'GAME'


states = {"GAME" : GameState(),
          "ENDG" : EndState(),
          "MENU" : MenuState(),
          "LOST" : LostState()}

current = "MENU"

@window.event
def on_key_press(symbol, modifiers):
    pressed[symbol] = True
    used[symbol] = False
    if symbol == pyglet.window.key.ESCAPE:
        return pyglet.event.EVENT_HANDLED

@window.event
def on_key_release(symbol, modifiers):
    pressed[symbol] = False
    used[symbol] = False

@window.event
def on_mouse_press(x, y, button, modifiers):
    global current
    current = states[current].process_event_mouse(x, y, button)

@window.event
def on_draw():
    global current
    window.clear()
    states[current].draw()
    
@window.event
def on_mouse_motion(x, y, dx, dy):
    utility.mouse_x = x
    utility.mouse_y = y

accum = 0

def update(dt):
    global current, accum
    accum += dt
    
    while accum >= STEP:
        current = states[current].update(STEP)
        if not states[current].player.playing:
            states[current].player.play()
        accum -= STEP
    window.set_caption("Zabudataja [" + str(int(1 / dt)) + "]")

pyglet.clock.schedule_interval(update, 1 / FPS)

pyglet.app.run()
