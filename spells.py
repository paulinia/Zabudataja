from constants import *
import utility
from math import sqrt, cos, sin, pi

#properties:
# self.v
# self.attack
# self.heal
# self.timestap
# self.radius

class SpellActive:
    def __init__(self, x_p, y_p, x, y, radius, batch, data, zoom = 2):
        self.active = False
        self.x = x_p
        self.y = y_p
        self.data = data
        self.sprite = pyglet.sprite.Sprite(self.data.image, x = x_p, y = y_p, batch = batch)
        self.image = data.image
        utility.scale_sprite(self, size / 2)
        self.wanted_position = utility.conventer(zoom, x_p, y_p, x, y)
        self.rotation = utility.rotate_to_position((x_p, y_p), self.wanted_position)
        self.expected_time = sqrt((self.wanted_position[0] - x_p) ** 2 + (self.wanted_position[1] - y_p) ** 2) / self.data.speed
        self.reduce_to_radius(radius, x_p, y_p)
    
    def reduce_to_radius(self, radius, x_p, y_p):
        if sqrt((self.wanted_position[0] - x_p) ** 2 + (self.wanted_position[1] - y_p) ** 2) > min(radius, self.data.max_radius):
            self.expected_time = min(radius, self.data.max_radius) / self.data.speed
    
    def update(self, dt):
        if not self.active:
            self.x += dt * self.data.speed * self.rotation[0]
            self.y += dt * self.data.speed * self.rotation[1]
            self.sprite.set_position(self.x, self.y)
            self.expected_time -= dt
            if self.expected_time <= 0:
                self.active = True
                
    def use(self, entity):
        #same spell never does both - it heals XOR attacks
        if entity.lives + self.data.heal >= entity.data.max_lives:
            entity.lives = entity.data.max_lives
        else:
            entity.lives += self.data.heal
        entity.lives -= self.data.attack
        
    def was_hit(self, entity):
        distance = utility.distance(self, entity)
        if distance <= self.data.radius:
            self.use(entity)
            return True
        return False

class Spell:
    def __init__(self, spell, path, name):
        self.spell = spell
        self.max_radius = 0
        with open(os.path.join(path, name + ".spell"), 'r') as sfile:
            i = 0
            for line in sfile:
                if i == 0:
                    self.name = line[:-1]
                elif i == 1:
                    self.speed = float(line)
                elif i == 2:
                    self.attack = float(line)
                elif i == 3:
                    self.timestap = float(line)
                elif i == 4:
                    self.radius = float(line)
                elif i == 5:
                    self.max_radius = float(line)
                i += 1
        
        self.heal = 0
        self.time_to_recover = 0
        self.image = pyglet.resource.image(os.path.join("graphics", self.name + ".png"))
        self.image.anchor_x, self.image.anchor_y = self.image.width // 2, self.image.height // 2
    
    def spell_it(self, x_p, y_p, x, y, radius, batch):
        if self.time_to_recover <= 0:
            self.time_to_recover = self.timestap
            return self.spell(x_p, y_p, x, y, radius, batch, self)
        else:
            return None
    
    def update(self, dt):
        if self.time_to_recover > 0:
            self.time_to_recover -= dt
            
    def get_info(self):
        text = [self.name, "Attack: " + str(self.attack), str(self.timestap) + " s"]
        return text
        

class SpellInventory:
    def __init__(self, spells = []):
        self.capacity = 3
        self.pointer = 0
        self.spells = [None for x in range(self.capacity)]
        for i in range(len(spells)):
            self.spells[i] = spells[i]
        
        self.keys = [(pyglet.window.mouse.LEFT, 'left'),
                     (pyglet.window.mouse.RIGHT, 'right'), 
                     (pyglet.window.mouse.MIDDLE, 'middle_button')]
        self.keys_to_pos = {}
        self.pic_keys = []
        self.batch = pyglet.graphics.Batch()
        self.spell_info = [(None, None) for x in range(self.capacity)]
        for i, key in enumerate(self.keys):
            self.keys_to_pos[key[0]] = i
            image = pyglet.resource.image("graphics/" + key[1] + ".png")
            image.anchor_x, image.anchor_y = size // 2, size // 2
            self.pic_keys.append(pyglet.sprite.Sprite(image, x = width - i * size - size // 2, y = size // 2, batch = self.batch))
            if len(spells) > i:
                self.spell_info[i] = (pyglet.sprite.Sprite(spells[i].image, x = width - i * size - size // 2, y = size // 2),
                                      [pyglet.text.Label(text, font_name='Times New Roman',
                                                        font_size = 16,
                                                        x = width - i * size - size, y = size + 80 - j * 20,
                                                        anchor_x='center', anchor_y='center') for j, text in enumerate(spells[i].get_info())])
        
        
        
    
    def add(self, spell):
        self.spells[self.pointer] = spell
        self.spell_info[self.pointer] = (pyglet.sprite.Sprite(spells[i].image, x = width - i * size - size // 2, y = size // 2),
                                         [pyglet.text.Label(text, font_name='Times New Roman',
                                                           font_size = 16,
                                                           x = width - i * size - size, y = size + 80 - j * 20,
                                                           anchor_x='center', anchor_y='center') for j, text in enumerate(spells[i].get_info())])
    
    def remove(self, spell):
        self.spells[self.pointer] = None
        self.spell_info[self.pointer] = (None, None)
    
    def update(self, dt):
        for spell in self.spells:
            if spell != None:
                spell.update(dt)
        
    def key_press(self, symbol):
        new_spells = []
        if used[symbol] == False:
            if symbol == 54:
                self.pointer = max(0, self.pointer - 1)
            if symbol == 53:
                self.pointer = min(self.capacity - 1, self.pointer + 1)
    
    def mouse_click(self, player, batch, button):
        new_spells = []
        if button in self.keys_to_pos:
            result = self.spell_it(player, batch, button)
            if result != None:
                new_spells.append(result)
        return new_spells
    
    def spell_it(self, player, batch, key):
        if self.spells[self.keys_to_pos[key]] != None:
            return self.spells[self.keys_to_pos[key]].spell_it(player.x, player.y, utility.mouse_x, utility.mouse_y, player.attack_radius, batch)
        return None
    
    def draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (width, 0,
                                                             width, size,
                                                             width - self.capacity * size, size,
                                                             width - self.capacity * size, 0)), ('c3B', (0, 255, 255) * 4))
        
        for i in range(self.capacity):
            if self.spells[i] != None:
                self.spell_info[i][0].draw()
                    
        self.batch.draw()
        
        if utility.mouse_y <= size and utility.mouse_x > width - self.capacity * size:
            poz_x = int((width - utility.mouse_x) // size)
            if self.spells[poz_x] == None:
                return ((width - utility.mouse_x) // size)
            if self.spells[poz_x] == None:
                return
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (width - poz_x * size, size + 100,
                                                                 width - poz_x * size - 2 * size, size + 100,
                                                                 width - poz_x * size - 2 * size, size,
                                                                 width - poz_x * size, size)), ('c3B', (255, 15, 25) * 4))
            for text in self.spell_info[poz_x][1]:
                text.draw()
        
        for i in range(self.capacity):
            if self.spells[i] != None and self.spells[i].time_to_recover > 0:
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (width - (i + 1) * size, 0,
                                                                     width - i * size, 0,
                                                                     width - i * size, size,
                                                                     width - (i + 1) * size, size)),
                ('c4B', (0, 0, 0, int(205 * self.spells[i].time_to_recover / self.spells[i].timestap) + 20) * 4))
