from constants import *
import utility

class Inventory:
    def __init__(self):
        self.capacity = 10
        self.items = []
        self.pointer = 0
        self.chosen = -1        
        self.keys = {pyglet.window.key.R : self.use,
                     pyglet.window.key.T : self.throw_away}
        
    
    def draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (0, 0,
                                                             self.capacity * size, 0,
                                                             self.capacity * size, size,
                                                             0, size)), ('c3B', (255, 255, 0) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (self.pointer * size, 0,
                                                             self.pointer * size + size, 0,
                                                             (self.pointer + 1) * size, size,
                                                             self.pointer * size, size)),
                                                                ('c3B', (0, 255, 255) * 4))
        if self.chosen != -1:
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (self.chosen * size + size // 2, 0,
                                                                 self.chosen * size + size, size // 2,
                                                                 self.chosen * size + size // 2, size,
                                                                 self.chosen * size, size // 2)), ('c3B', (255, 0, 255) * 4))
 
        for i in range(0, self.capacity):
            if len(self.items) > i:
                self.items[i].draw(i * size + size // 2, size // 2)
                
        if utility.mouse_y <= size and utility.mouse_x < size * len(self.items):
            poz_x = int(utility.mouse_x // size)
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (poz_x * size, size,
                                                                 poz_x * size + 2 * size, size,
                                                                 poz_x * size + 2 * size, size + 100,
                                                                 poz_x * size, size + 100)), ('c3B', (255, 255, 255) * 4))
            texts = self.items[poz_x].data.get_info(poz_x * size + size, size + 50)
            for text in texts:
                text.draw()
    
    def move_pointer(self, key, player):
        if key == pyglet.window.key.E:
            self.pointer = (self.capacity + self.pointer + 1) % self.capacity
        if key == pyglet.window.key.Q:
            self.pointer = (self.capacity + self.pointer - 1) % self.capacity
        
        if key in self.keys:
            self.keys[key](player)
    
    def use(self, player):
        if self.pointer < len(self.items):
            self.items[self.pointer].use(player)
            if self.items[self.pointer].data.type_of == 'E':
                self.chosen = self.pointer
            if self.items[self.pointer].data.type_of == 'I':
                self.throw_away(player)
    
    def throw_away(self, player):
        if self.pointer < len(self.items):
            self.items.pop(self.pointer)
        if self.chosen == self.pointer:
            self.chosen = -1
            player.set_to_default
        if self.pointer < self.chosen:
            self.chosen -= 1

    
    def collect(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False
