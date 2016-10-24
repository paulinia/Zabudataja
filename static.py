from constants import *

class Tile:
    def __init__(self, x, y, batch):
        self.tile_imag = pyglet.resource.image(os.path.join("graphics", "tile.png"))
        self.tile_imag.anchor_x = 0
        self.tile_imag.anchor_y = 0
        self.sprite = pyglet.sprite.Sprite(self.tile_imag, x = x, y = y, usage = 'static', batch = batch)
    
class Wall:
    def __init__(self, x, y, batch):
        self.tile_imag = pyglet.resource.image(os.path.join("graphics", "wall.png"))
        self.tile_imag.anchor_x = 0
        self.tile_imag.anchor_y = 0
        #docasne
        self.sprite = pyglet.sprite.Sprite(self.tile_imag, x = x, y = y, usage = 'static', batch = batch)
        
class Portal:
    def __init__(self, x, y, batch, level, opened):
        self.level = level
        if opened:
            self.image = pyglet.resource.image(os.path.join("graphics", "door_opened.png"))
        else:
            self.image = pyglet.resource.image(os.path.join("graphics", "door.png"))
        self.opened = opened
        self.image.anchor_x, self.image.anchor_y = 0, 0
        self.sprite = pyglet.sprite.Sprite(self.image, x = x, y = y, usage = 'static', batch = batch)
    
    def acces(self, inventory):
        if self.opened:
            return False
        for item in inventory.items:
            if item.data.type_of == 'K':
                self.sprite.image = pyglet.resource.image(os.path.join("graphics", "door_opened.png"))
                return True
        return False
