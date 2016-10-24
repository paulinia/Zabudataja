from constants import *
import os

class Enemy:
    def __init__(self, load = False, path = None, name = None, batch = None, pics = None):
        self.load = load
        if load:
            self.name = name
            efile = open(path + name + '.enemy', 'r')
            lines = efile.readlines()
            for pos in lines[9:]:
                x, y = map(float, pos.split())
                pics.append(pyglet.sprite.Sprite(pyglet.resource.image("graphics/" + name + ".png"), x = x * size, y = y * size, batch = batch))
            return
            
        self.name = input("Enter enemy's name: ")
        if self.name == '':
            return None
        self.attack = int(input("Enter " + self.name + "'s attack: "))
        self.recover_speed = int(input("Enter " + self.name + "'s recover speed: "))
        self.radio = int(input("Enter " + self.name + "'s movement radio: "))
        self.lives = int(input("Enter " + self.name + "'s maximum number of lives: "))
        self.speed = int(input("Enter " + self.name + "'s speed: "))
        self.number_of_spawned_items = int(input("Enter " + self.name + "'s spawned items: "))
        self.items = input("Enter items: [one character]: ")
        self.positions = []
        
    def add(self, x, y, pics, batch):
        self.positions.append((x, y))
        pics.append(pyglet.sprite.Sprite(pyglet.resource.image("graphics/" + self.name + ".png"), x = x * size, y = y * size, batch = batch))
    
    def write_to_file(self, path):
        if self.load:
            return self.name
        
        with open(path + self.name + ".enemy", 'w') as enemy_file:
            enemy_file.write(self.name + "\n")
            enemy_file.write(str(self.attack) + "\n")
            enemy_file.write(str(self.recover_speed) + "\n")
            enemy_file.write(str(self.radio) + "\n")
            enemy_file.write(str(self.lives) + "\n")
            enemy_file.write(str(self.speed) + "\n")
            enemy_file.write(str(self.number_of_spawned_items) + "\n")
            enemy_file.write(self.items + '\n')
            enemy_file.write(str(len(self.positions)) + "\n")
            for pos in self.positions:
                enemy_file.write(str(pos[0]) + " " + str(pos[1]) + "\n")
        
        return self.name

class Spell:
    def __init__(self):
        self.spells = []
        self.loaded = []
    
    def add(self, load = False, name = None):
        
        if load:
            self.spells.append([name])
            self.loaded.append(True)
            return
        
        name = str(input("Enter spell name: "))
        if name == '':
            return
        speed = input("Enter " + name + "'s speed: ")
        attack = input("Enter " + name + "'s attack: ")
        #heal maybe?
        time = input("Enter " + name + "'s timestap: ")
        radius = input("Enter " + name + "'s attack radio: ")
        mxradius = input("Enter " + name + "'s maximum radio: ")
        self.spells.append((name, speed, attack, time, radius, mxradius))
        self.loaded.append(False)
    
    def write_to_file(self, path):
        for i, spell in enumerate(self.spells):
            if self.loaded[i]:
                continue
            
            with open(path + spell[0]+ ".spell", 'w') as spell_file:
                spell_file.write(spell[0] + "\n")
                spell_file.write(spell[1] + "\n")
                spell_file.write(spell[2] + "\n")
                spell_file.write(spell[3] + "\n")
                spell_file.write(spell[4] + "\n")
                spell_file.write(spell[5] + "\n")
            
        
        return [spell[0] for spell in self.spells]

class Grandma:
    def __init__(self, new = True, path = None, batch = None, pics = None):
        self.positions = []
        self.messages = []
        if not new:
            i = 1
            gfile = open(path + "grandma.info")
            lines = gfile.readlines()
            while i < len(lines):
                self.positions.append(tuple(map(float, lines[i].split())))
                x, y = self.positions[-1]
                pics.append(pyglet.sprite.Sprite(pyglet.resource.image("graphics/house.png"), x = x * size, y = y * size, batch = batch))
                m = int(lines[i + 1])
                i += 1
                self.messages.append(lines[i + 1 : i + 1 + m])
                i = i + 1 + m
            
    
    def add(self, x, y, pics, batch):
        self.positions.append((x, y))
        self.messages.append(input("Enter grandma's message: ").split("... "))
        pics.append(pyglet.sprite.Sprite(pyglet.resource.image("graphics/house.png"), x = x * size, y = y * size, batch = batch))
        print(self.messages)
        
    def write_to_file(self, path):
        with open(path + "grandma.info", 'w') as grandma_file:
            grandma_file.write(str(len(self.positions)) + "\n")
            for i, poz in enumerate(self.positions):
                grandma_file.write(str(poz[0]) + " " + str(poz[1]) + "\n")
                grandma_file.write(str(len(self.messages[i])) + '\n')
                for text in self.messages[i]:
                    grandma_file.write(text)
                    if text[-4:-1] == '...':
                        if text[-1] != '\n':
                            grandma_file.write('\n')
                    else:
                        grandma_file.write('...\n')

class Item:
    def __init__(self):
        self.items = []
        self.loaded = []
    
    def add(self, load = False, name_of = None):
        if load:
            self.items.append([name_of])
            self.loaded.append(True)
            return
        
        name = str(input("Enter item name: "))
        if name == '':
            return
        shortcut = input("Enter [one-character-long] shortcut: ")
        type_of_item = input("Enter type of item [if equipment 'E' if instants enter 'I' if key 'K']: ")
        if type_of_item == 'I':
            self.items.append((name, shortcut, 'I', input("Enter " + name + "'s heal: ")))
        elif type_of_item == 'E':
            speed = input("Enter player's speed with this equip: ")
            defense = input("Enter fraction of reduced attack: ")
            recover = input("Enter recover speed with this equip: ")
            radio = input("Enter attack radio of player with this equip: ")
            self.items.append((name, shortcut, 'E', speed, defense, recover, radio))
        elif type_of_item == 'K':
            self.items.append((name, shortcut, 'K'))
        self.loaded.append(False)
    
    def write_to_file(self, path):
        for i, item in enumerate(self.items):
            if self.loaded[i]:
                continue
            
            with open(path + item[0] + ".item", 'w') as item_file:
                if item[2] == 'I':
                    item_file.write(item[0] + "\n")
                    item_file.write(item[1] + "\n")
                    item_file.write(item[2] + "\n")
                    item_file.write(item[3] + "\n")
                if item[2] == 'E':
                    item_file.write(item[0] + "\n")
                    item_file.write(item[1] + "\n")
                    item_file.write(item[2] + "\n")
                    item_file.write(item[3] + "\n")
                    item_file.write(item[4] + "\n")
                    item_file.write(item[5] + "\n")
                    item_file.write(item[6] + "\n")
                if item[2] == 'K':
                    item_file.write(item[0] + "\n")
                    item_file.write(item[1] + "\n")
                    item_file.write(item[2] + "\n")
            
        
        return [item[0] for item in self.items]

class Level:
    def create_level(self, path):
        self.path = path
        self.n = int(input("Rozmer levelu: "))
        self.mapa = [[1 for y in range(self.n)] for x in range(self.n)]
        self.walls = [[None for y in range(self.n)] for x in range(self.n)]
        self.enemies = []
        self.grandmas = Grandma()
        self.items = Item()
        self.spells = Spell()
        self.batch_static, self.batch_entity, self.batch_tiles = pyglet.graphics.Batch(), pyglet.graphics.Batch(), pyglet.graphics.Batch()
        self.static = []
        self.pics = []
        tile_image = pyglet.resource.image("graphics/tile.png")
        self.image = pyglet.resource.image("graphics/wall.png")
        self.player_pos = [(0, 0, None), (0, 0, None)]
        self.it = 0
        self.default = None
        for i in range(self.n):
            for j in range(self.n):
                self.static.append(pyglet.sprite.Sprite(tile_image, x = j * size, y = i * size, usage = 'static', batch = self.batch_tiles))
    
    def load_level(self, path):
        self.path = path
        lfile = open(self.path + "level.data", 'r')
        lines = lfile.readlines()
        self.n = int(lines[0])
        self.mapa = [[1 for y in range(self.n)] for x in range(self.n)]
        self.walls = [[None for y in range(self.n)] for x in range(self.n)]
        self.enemies = []
        self.items = Item()
        self.spells = Spell()
        self.batch_static, self.batch_entity, self.batch_tiles = pyglet.graphics.Batch(), pyglet.graphics.Batch(), pyglet.graphics.Batch()
        self.static = []
        self.pics = []
        tile_image = pyglet.resource.image("graphics/tile.png")
        self.image = pyglet.resource.image("graphics/wall.png")
        self.player_pos = [(0, 0, None), (0, 0, None)]
        self.it = 0
        self.spells = Spell()
        self.player = (None, None)
        self.mapa = [[1 for y in range(self.n)] for x in range(self.n)]
        j = 0
        for line in lines[1 : 1 + self.n]:
            i = 0
            for c in line[:-1]:
                self.mapa[i][j] = int(c)
                self.static.append(pyglet.sprite.Sprite(tile_image, x = i * size, y = j * size, batch = self.batch_tiles))
                if c == '0':
                    self.walls[i][j] = pyglet.sprite.Sprite(self.image, x = i * size, y = j * size, batch = self.batch_static)
                i += 1
            j += 1
        
        en = int(lines[self.n + 4])
        
        for name in lines[self.n + 5 : self.n + 5 + en]:
            self.enemies.append(Enemy(True, self.path, name[:-1], self.batch_entity, self.pics))
        
        self.default = tuple(map(float, lines[1 + self.n].split()))
        x1, y1 = map(float, lines[2 + self.n].split())
        x2, y2 = map(float, lines[3 + self.n].split())
        imageP = pyglet.resource.image("graphics/player.png")
        imageD = pyglet.resource.image("graphics/door.png")
        self.player_pos = [(x1, y1, pyglet.sprite.Sprite(imageP, x = x1 * size, y = y1 * size, batch = self.batch_entity)),
                           (x2, y2, pyglet.sprite.Sprite(imageD, x = x2 * size, y = y2 * size, batch = self.batch_entity))]
        
        es = int(lines[self.n + 5 + en])
        
        for name in lines[self.n + 6 + en : self.n + 6 + en + es]:
            self.spells.add(True, name[:-1])
            
        ei = int(lines[self.n + 6 + en + es])
        
        li = es + en + self.n
        
        for name in lines[li + 7 : li + 7 + ei]:
            self.items.add(True, name[:-1])
        
        self.grandmas = Grandma(False, path, self.batch_static, self.pics)
    
    def draw(self):
        self.batch_tiles.draw()
        self.batch_static.draw()
        self.batch_entity.draw()
    
    def key_press(self, mode):
        if mode == 'ENEMY':
            new = Enemy()
            if new.name != '':
                self.enemies.append(new)
                self.mode = None
        if mode == 'SPELL':
            self.spells.add()
        if mode == 'ITEM':
            self.items.add()
        if mode == 'PLAYER':
            speed = input("Enter player's speed: ")
            if speed == '':
                return
            recover = input("Enter player's recover speed: ")
            max_lives = input("Enter player's maximum lives: ")
            self.default = (speed, recover, 0, 0, 0, max_lives)
            self.it = 0
    
    def add_entity(self, mode, x, y):
        if x < 0 or x >= self.n or y < 0 or y >= self.n:
            return
        if mode == "WALL":
            self.walls[int(x)][int(y)] = pyglet.sprite.Sprite(self.image, x = x * size, y = y  * size, usage = 'static', batch = self.batch_static)
            self.mapa[int(x)][int(y)] = 0
        if mode == "DEMOLISH":
            if self.walls[int(x)][int(y)] != None:
                self.walls[int(x)][int(y)].delete()
            self.walls[int(x)][int(y)] = None
            self.mapa[int(x)][int(y)] = 1
        if mode == 'ENEMY':
            self.enemies[-1].add(x, y, self.pics, self.batch_entity)
        if mode == 'GRANDMA':
            self.grandmas.add(x, y, self.pics, self.batch_entity)
        if mode == 'PLAYER':
            image = None
            if self.it == 0:
                image = pyglet.resource.image("graphics/player.png")
            elif self.it == 1:
                image = pyglet.resource.image("graphics/door.png")
            else:
                return
            self.player_pos[self.it] = (x, y, pyglet.sprite.Sprite(image, x = x * size, y = y * size, batch = self.batch_entity))
            self.it += 1
    
    def write_to_file(self):
        with open(self.path + "level.data", 'w') as lfile:
            lfile.write("{}\n".format(self.n))
            for i in range(self.n):
                for j in range(self.n):
                    lfile.write(str(self.mapa[j][i]))
                lfile.write("\n")
            
            lfile.write("{} {} {} {} {} {}\n{} {}\n{} {}\n".format(self.default[0], self.default[1], self.default[2], self.default[3], 
                                                                 self.default[4], self.default[5], self.player_pos[0][0], self.player_pos[0][1],
                                                                 self.player_pos[1][0], self.player_pos[1][1]))
            lfile.write("{}\n".format(len(self.enemies)))
            for enemy in self.enemies:
                enemy.write_to_file(self.path)
                lfile.write("{}\n".format(enemy.name))
            
            lfile.write("{}\n".format(len(self.spells.spells)))
            self.spells.write_to_file(self.path)
            for spell in self.spells.spells:
                lfile.write("{}\n".format(spell[0]))
            
            lfile.write("{}\n".format(len(self.items.items)))
            self.items.write_to_file(self.path)
            for item in self.items.items:
                lfile.write("{}\n".format(item[0]))
                
            self.grandmas.write_to_file(self.path)
            f = open(self.path + "time.info", 'a')
            f.write("-1\n")
            f = open(self.path + "text", 'a')
            f.write("  ")
                
