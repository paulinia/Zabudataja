from constants import *

class NonPlayableCharacterHouse:
    def __init__(self, npc, x, y, batch):
        self.character = npc
        self.x = x
        self.y = y
        self.image = pyglet.resource.image(os.path.join("graphics", "house.png"))
        self.sprite = pyglet.sprite.Sprite(self.image, x = x, y = y, batch = batch, usage = 'static')
    
    def come_in(self, level):
        level.in_house = self
    
    def draw(self, level):
        x, y = self.character.draw()
        level.player.draw(x, y)
    
    def click(self, x, y, button, level):
        if self.character.click(x, y, button, level):
            level.in_house = None
    
class Grandma:
    def __init__(self, message):
        self.message = message
        self.image = pyglet.resource.image(os.path.join("graphics", "grandma.png"))
        self.image.anchor_x, self.image.anchor_y = self.image.width // 2, self.image.height // 2
        self.sprite = pyglet.sprite.Sprite(self.image, width // 2, height // 2)
        self.sprite.scale = 1
        self.it = -1
        texts = self.message
        x = self.sprite.x + 6 * size
        y = self.sprite.y + 2 * size
        self.texts = [[pyglet.text.Label(list_s[i], font_name = 'Times New Roman', font_size = 20,
                                         x = x, y = y + (15 * len(list_s) + 15) - i * 35, anchor_x = 'center', anchor_y = 'center',
                                         color = (0, 0, 0, 255)) for i in range(len(list_s))] for list_s in texts]
        
    def draw(self):
        self.sprite.draw()
        if(self.it > -1):
            length = 30
            x = self.sprite.x
            y = self.sprite.y
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x, y + size, x, y + size,
                                                                 3 * size + x, y + size,
                                                                 3 * size + x, y + size + length)), ('c3B', (255, 255, 255) * 4))
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x + 3 * size, y - 3 * size,
                                                                 x + 9 * size, y - 3 * size,
                                                                 x + 9 * size, y + 6 * size,
                                                                 x + 3 * size, y + 6 * size)), ('c3B', (255, 255, 255) * 4))
            for label in self.texts[self.it]:
                label.draw()
                
        return 500, 200;
    
    def click(self, x, y, button, level):
        self.it += 1
        if self.it >= len(self.message):
            self.it = -1
            return True
        return False
