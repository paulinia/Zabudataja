from constants import *
import utility

class Item:
    def __init__(self, x, y, batch, data):
        self.sprite = pyglet.sprite.Sprite(data.image, x = x, y = y, batch = batch)
        self.on_map = True
        self.data = data
        self.image = data.image
    
    def collect(self):
        self.on_map = False
        utility.destroy(self)
        self.sprite = pyglet.sprite.Sprite(self.data.image)
        utility.scale_sprite(self, size)
        
    def draw(self, x, y):
        if self.on_map:
            return
        self.sprite.set_position(x, y)
        self.sprite.draw()
    
    def use(self, player):
        if not self.on_map:
            player.use(self)
    
    def rotate(self):
        pass

class ItemData:
    def spawn(self, x, y, batch):
        item = Item(x, y, batch, self)
        utility.scale_sprite(item, size / 2)
        return item
    
class ItemDataInstant(ItemData):
    def __init__(self, name, heal):
        self.type_of = "I"
        self.name = name
        self.heal = heal
        self.image = pyglet.resource.image(os.path.join("graphics", name + ".png"))
        self.image.anchor_x, self.image.anchor_y = self.image.width // 2, self.image.height // 2
    
    def get_info(self, x, y): #x, y = center's
        texts = [pyglet.text.Label(self.name, font_name = 'Times New Roman', font_size = 20, x = x, y = y + 20,
                                   anchor_x = 'center', anchor_y = 'center', color = (0, 0, 0, 255)),
                 pyglet.text.Label("health: " + str(self.heal), font_name = 'Times New Roman', 
                                   font_size = 20, x = x, y = y - 20, anchor_x = 'center', anchor_y = 'center', color = (0, 0, 0, 255))]
        return texts


class ItemDataKey(ItemData):
    def __init__(self, name):
        self.type_of = "K"
        self.name = name
        self.image = pyglet.resource.image(os.path.join("graphics", name + ".png"))
        self.image.anchor_x, self.image.anchor_y = self.image.width // 2, self.image.height // 2
    
    def get_info(self, x, y): #x, y = center's
        texts = [pyglet.text.Label(self.name, font_name = 'Times New Roman', font_size = 20, x = x, y = y + 20,
                                   anchor_x = 'center', anchor_y = 'center', color = (0, 0, 0, 255)),
                 pyglet.text.Label("Unlocks door", font_name = 'Times New Roman', 
                                   font_size = 16, x = x, y = y - 20, anchor_x = 'center', anchor_y = 'center', color = (0, 0, 0, 255))]
        return texts
    
class ItemDataEquipment(ItemData): #   player's speed     % of reduced attack     recovering speed  radius
    def __init__(self, name,           velocity,          defense,                recover_speed,    attack_radius):
        self.type_of = "E"
        self.name = name
        self.velocity = velocity
        self.defense = defense
        self.attack_radius = attack_radius
        self.recover_speed = recover_speed
        self.image = pyglet.resource.image(os.path.join("graphics", name + ".png"))
        self.image.anchor_x, self.image.anchor_y = self.image.width // 2, self.image.height // 2
    
    def get_info(self, x, y):
        texts = [pyglet.text.Label(self.name, font_name = 'Times New Roman', font_size = 16, x = x, y = y + 40,
                                   anchor_x = 'center', anchor_y = 'center', color = (0, 0, 0, 255)),
                 pyglet.text.Label("velocity: " + str(self.velocity), font_name = 'Times New Roman', 
                                   font_size = 16, x = x, y = y + 20, anchor_x = 'center', anchor_y = 'center', color = (0, 0, 0, 255)),
                 pyglet.text.Label("defense: " + str(self.defense), font_name = 'Times New Roman', 
                                   font_size = 16, x = x, y = y, anchor_x = 'center', anchor_y = 'center', color = (0, 0, 0, 255)),
                 pyglet.text.Label("radius: " + str(self.attack_radius), font_name = 'Times New Roman', 
                                   font_size = 16, x = x, y = y - 20, anchor_x = 'center', anchor_y = 'center', color = (0, 0, 0, 255)),
                 pyglet.text.Label("recover: " + str(self.recover_speed), font_name = 'Times New Roman',
                                   font_size = 16, x = x, y = y - 40, anchor_x = 'center', anchor_y = 'center', color = (0, 0, 0, 255))]
        return texts

#list of
list_of_items = {}
