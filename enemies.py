from constants import *
import random
import livebar
import items

class Enemy:
    def __init__(self, x, y, min_x, min_y, max_x, max_y, batch, data):
        self.data = data
        self.lives = data.max_lives
        self.x = x
        self.y = y
        self.rotation = random.randint(0, 3)
        self.livebar = livebar.Livebar(self.data.max_lives)
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.load_graphics(batch)
    
    def load_graphics(self, batch):
        self.image = pyglet.resource.image(os.path.join("graphics", self.data.name + ".png"))
        self.image.anchor_y, self.image.anchor_x = self.image.height // 2, self.image.width // 2
        self.sprite = pyglet.sprite.Sprite(self.image, x = self.x, y = self.y, batch = batch)
        self.sprite.scale = (54 / max(self.image.height, self.image.width))
        
    def move(self, dt):
        self.lives += dt * self.data.recover_speed
        if self.lives > self.data.max_lives:
            self.lives = self.data.max_lives
        
        self.x += D[symbols[self.rotation]][0] * dt * self.data.velocity
        self.y += D[symbols[self.rotation]][1] * dt * self.data.velocity
        
        if random.randint(0, 100) == 0:
            self.rotate()
        
        self.livebar.set_lives(self.lives)
        if self.x < self.min_x:
            self.x = self.min_x
            self.rotate()
        if self.y < self.min_y:
            self.y = self.min_y
            self.rotate()
        if self.x > self.max_x:
            self.x = self.max_x
            self.rotate()
        if self.y > self.max_y:
            self.y = self.max_y
            self.rotate()
        self.sprite.set_position(self.x, self.y)
    
    def rotate(self):
        self.rotation = random.randint(0, 3)
        self.sprite.rotation = self.rotation * 90
        
    def is_dead(self, items_on_map):
        if self.lives <= 0:
            self.die(items_on_map)
            return True
        else:
            return False
    
    def draw(self):
        self.livebar.draw(self.x, self.y)
    
    def die(self, items_on_map):
        for i in range(0, self.data.num_of_spawned_items):
            items_on_map.append(items.list_of_items[random.choice(self.data.to_spawn)].spawn(self.x + random.randint(-size, size),
                                                                                             self.y + random.randint(-size, size),
                                                                                             self.sprite.batch))
        #casom to bude fiiikanejsie


class EnemyData:
    def __init__(self, path, name):
        proper = []
        with open(os.path.join(path, name + ".enemy"), 'r') as efile:
            for line in efile:
                proper.append(str(line))
        self.name = proper[0][:-1]
        self.attack = int(float(proper[1]))
        self.recover_speed = int(float(proper[2]))
        self.radio = int(float(proper[3]))
        self.max_lives = int(float(proper[4]))
        self.velocity = int(float(proper[5]))
        self.num_of_spawned_items = int(float(proper[6]))
        self.to_spawn = proper[7].split()
        self.n = int(float(proper[8]))
        self.positions = [list(map(float, proper[x].split())) for x in range(9, 9 + self.n)]
        self.i = 0
        
    def create_entity(self, batch):
        if self.i < self.n:
            entity = Enemy(self.positions[self.i][0] * size, self.positions[self.i][1] * size, (self.positions[self.i][0] - self.radio) * size,
                           (self.positions[self.i][1] - self.radio) * size, (self.positions[self.i][0] + self.radio) * size,
                           (self.positions[self.i][1] + self.radio) * size, batch, self)
            self.i += 1
            return entity
        else:
            return None
