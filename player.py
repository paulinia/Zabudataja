from constants import *
import livebar
import spells
import utility

class Player:
    def __init__(self, x, y, batch):
        self.x = x
        self.y = y
        self.velocity = 100
        self.recover_speed = 5
        self.image = pyglet.resource.image(os.path.join("graphics", "player.png"))
        self.image.anchor_x, self.image.anchor_y = self.image.width // 2, self.image.height // 2
        self.sprite = pyglet.sprite.Sprite(self.image, x = x, y = y, batch = batch)
        self.lives = 100
        self.max_lives = self.lives
        self.livebar = livebar.Livebar(self.max_lives)
        self.mana = 0 #will be used later
        self.defense = 0
        self.default = (100, 5, 0, 0, 0, 100)
        self.attack_radius = 0
        
    def draw(self, x = None, y = None):
        if self.is_dead():
            return
        if x == None:
            self.livebar.draw(self.x, self.y)
        else:
            self.livebar.draw(x, y)
            pyglet.sprite.Sprite(self.image, x, y).draw()
        
    def move(self, dt, symbol):
        if symbol == pyglet.window.key.W:
            self.sprite.rotation = 0
        if symbol == pyglet.window.key.D:
            self.sprite.rotation = 90
        if symbol == pyglet.window.key.S:
            self.sprite.rotation = 180
        if symbol == pyglet.window.key.A:
            self.sprite.rotation = 270
        self.x += D[symbol][0] * dt * self.velocity
        self.y += D[symbol][1] * dt * self.velocity
        self.sprite.set_position(self.x, self.y)
        
    def key_press(self, symbol):
        pass
    
    def update(self, dt):
        self.lives += self.recover_speed * dt
        if self.lives > self.max_lives:
            self.lives = self.max_lives
        self.livebar.set_lives(self.lives)
    
    def enemy_attack(self, attack, dt):
        self.lives -= attack * dt - (attack * dt * self.defense)
        self.livebar.set_lives(self.lives)
        return self.is_dead()
            
    def is_dead(self):
        if self.lives <= 0:
            self.die()
            return True
        else:
            return False
    
    def die(self):
        self.sprite.image = pyglet.resource.image(os.path.join("graphics", "dead.png"))
        self.velocity = 0
        #casom to bude fiiikanejsie
        
    def rotate(self):
        pass
    
    def use(self, item):
        if item.data.type_of == 'I':
            self.lives += item.data.heal
            if self.lives > self.max_lives:
                self.lives = self.max_lives
            self.livebar.set_lives(self.lives)
        if item.data.type_of == 'E':
            self.velocity = item.data.velocity
            self.recover_speed = item.data.recover_speed
            self.defense = item.data.defense
            self.attack_radius = item.data.attack_radius
        if item.data.type_of == 'K':
            pass
    
    def position(self):
        return (self.x, self.y)
    
    def set_to_default(self):
        self.velocity = self.default[0]
        self.recover_speed = self.default[1]
        self.defense = self.default[2]
        self.mana = self.default[3]
        self.attack_radius = self.default[4]
        self.max_lives = self.default[5]
