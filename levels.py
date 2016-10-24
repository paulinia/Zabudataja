from constants import *
import random
import enemies
import static
import player
import items
import utility
import inventory
import camera
import npc
import spells
from time import sleep

class Level:
    def __init__(self, num):
        self.path = os.path.join("levels", num);
        self.id_level = num
        self.load()
    
    def load(self):
        self.timer = 0
        self.darkened = 0
        self.darken_speed = 0
        with open(os.path.join(self.path, 'time.info'), 'r') as tfile:
            for line in tfile:
                if float(line) <= 0:
                    self.darken_speed = 0
                else:
                    self.darken_speed = 255 / float(line)
        if self.id_level == '13':
            self.darkened = 2 * 255 / 3
        elif self.id_level == '12':
            self.darkened = 255 / 2
        self.walls = []
        self.houses = []
        self.tiles = []
        self.player_x = 2
        self.player_y = 2
        self.static_batch = pyglet.graphics.Batch()
        self.entities_batch = pyglet.graphics.Batch()
        self.npc_batch = pyglet.graphics.Batch()
        self.exit = None
        self.enter = None
        self.types_of_enemies = []
        self.enemies = []
        to_spell_inventory = []
        
        self.to_recover = None
        
        nume = 0
        nums = 0
        numi = 0
        
        with open(os.path.join(self.path, "level.data"), 'r') as lfile:
            it = 0
            for line in lfile:
                if it == 0:
                    self.n = int(float(line))
                    self.land = [[0 for x in range(self.n)] for x in range(self.n)]
                if it > 0 and it < self.n + 1:
                    i = 0
                    for c in line[:-1]:
                        if c == '1':
                            self.land[i][it - 1] = 1
                            self.tiles.append(static.Tile(i * size, (it - 1) * size, self.static_batch))
                        else:
                            self.walls.append(static.Wall(i * size, (it - 1) * size, self.static_batch))
                        i += 1
                if it == self.n + 1:
                    self.proper = list(map(int, list(map(float, line.split()))))
                if it == self.n + 2:
                    pos = list(map(int, list(map(float, line.split()))))
                    self.player_x = pos[0]
                    self.player_y = pos[1]
                    self.player = player.Player(self.player_x * size + size // 2, self.player_y * size + size // 2, self.entities_batch)
                    self.player.default = (self.proper[0], self.proper[1], self.proper[2], self.proper[3], self.proper[4], self.proper[5])
                    self.player.set_to_default()
                    self.enter = static.Portal(self.player_x * size, self.player_y * size, self.npc_batch, 0, True)
                if it == self.n + 3:
                    pos = list(map(int, list(map(float, line.split()))))
                    self.exit = static.Portal(pos[0] * size, pos[1] * size, self.npc_batch, 1, False)
                    self.land[pos[0]][pos[1]] = 2
                if it == self.n + 4:
                    nume = int(line)
                if it < self.n + 5 + nume and it > self.n + 4:
                    self.types_of_enemies.append(enemies.EnemyData(self.path, str(line[:-1])))
                    entity = self.types_of_enemies[-1].create_entity(self.entities_batch)
                    while entity != None:
                        self.enemies.append(entity)
                        entity = self.types_of_enemies[-1].create_entity(self.entities_batch)
                if it == self.n + 5 + nume:
                    nums = int(line)
                if it > self.n + 5 + nume and it < self.n + 6 + nume + nums:
                    to_spell_inventory.append(spells.Spell(spells.SpellActive, self.path, line[:-1]))
                if it == self.n + 6 + nume + nums:
                    numi = int(line)
                if it > self.n + 6 + nume + nums and it < self.n + 7 + nums + nume + numi:
                    f = open(os.path.join(self.path, line[:-1] + '.item'), 'r')
                    lines = f.readlines()
                    if lines[2][:-1] == 'K':
                        items.list_of_items[lines[1][:-1]] = items.ItemDataKey(lines[0][:-1])
                    if lines[2][:-1] == 'E':
                        items.list_of_items[lines[1][:-1]] = items.ItemDataEquipment(lines[0][:-1], float(lines[3][:-1]), float(lines[4][:-1]),
                                                                                   float(lines[5][:-1]), float(lines[6][:-1]))
                    if lines[2][:-1] == 'I':
                        items.list_of_items[lines[1][:-1]] = items.ItemDataInstant(lines[0][:-1], float(lines[3][:-1]))
                
                it += 1
                
        
        gfile = open(os.path.join(self.path, "grandma.info"), 'r')
        lines = gfile.readlines()
        it = 1
        while it < len(lines):
            x, y = map(float, lines[it].split())
            it += 1
            m = int(lines[it])
            messages = []
            for i in range(it + 1, it + 1 + m):
                messages.append(utility.split(21, lines[i][:-1]))
            self.houses.append(npc.NonPlayableCharacterHouse(npc.Grandma(messages), x * size, y * size, self.npc_batch))
            self.land[int(x)][int(y)] = 2 + len(self.houses)
            it = it + 1 + m
        
        self.inventory = inventory.Inventory()
        
        self.spell_inventory = spells.SpellInventory(to_spell_inventory)
        
        self.active_spells = []
        self.active_items = []
        self.casted_spells = []
        
        self.camera_game = camera.Camera(width, height, (self.player.x, self.player.y), 2)
        self.camera = camera.Camera(width, height, (width / 2, height / 2), 1)
        self.in_house = None
        
    def draw(self):
        if self.in_house == None:
            self.camera_game.position = self.player.position()
            self.camera_game.begin()
            
            self.static_batch.draw()
            self.npc_batch.draw()
            self.entities_batch.draw()
            
            self.player.draw()
            for enemy in self.enemies:
                enemy.draw()
                
            self.camera_game.end()
        else:
            self.camera.begin()
            self.in_house.draw(self)
            self.camera.end()
        
        self.camera.begin()
        self.inventory.draw()
        self.spell_inventory.draw()
        
        if self.in_house == None:
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (0, 0, width, 0,
                                                                 width, height, 0, height)), ('c4B', (0, 0, 0, min(255, int(self.darkened))) * 4))
        
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (utility.mouse_x, utility.mouse_y,
                                                             utility.mouse_x - 6, utility.mouse_y - 12,
                                                             utility.mouse_x, utility.mouse_y - 6,
                                                             utility.mouse_x + 6, utility.mouse_y - 12)), ('c3B', (255, 20, 20) * 4))
        
        self.camera.end()
    
    def process_collision(self, entity):
        position = utility.field_of(entity.x + entity.sprite.scale * entity.image.width // 2,
                                    entity.y + entity.sprite.scale * entity.image.height // 2)
        if self.land[int(position[0])][int(position[1])] == 0:
            utility.process_collision(entity, position)
            entity.rotate()
        position = utility.field_of(entity.x - entity.sprite.scale * entity.image.width // 2, 
                                    entity.y + entity.sprite.scale * entity.image.height // 2)
        if self.land[int(position[0])][int(position[1])] == 0:
            utility.process_collision(entity, position)
            entity.rotate()
        position = utility.field_of(entity.x + entity.sprite.scale * entity.image.width // 2,
                                    entity.y - entity.sprite.scale * entity.image.height // 2)
        if self.land[int(position[0])][int(position[1])] == 0:
            utility.process_collision(entity, position)
            entity.rotate()
        position = utility.field_of(entity.x - entity.sprite.scale * entity.image.width // 2, 
                                    entity.y - entity.sprite.scale * entity.image.height // 2)
        if self.land[int(position[0])][int(position[1])] == 0:
            utility.process_collision(entity, position)
            entity.rotate()

    def update(self, dt):
        
        if self.to_recover != None and self.to_recover > 0:
            self.to_recover -= dt
            return
        if self.to_recover != None and self.to_recover <= 0:
            self.replay()
            return "REPL"
        
        self.timer += dt
        
        if self.player.is_dead():
            utility.player_effects.queue(audio_effects["DEAD"])
            utility.player_effects.play()
            if self.id_level == '13' and len(self.enemies) == 2:
                return "SACR"
            self.to_recover = 0.5
        
        #if player is in house state, you can just click
        if self.in_house:
            return
        
        self.darkened += self.darken_speed * dt
        
        pos = utility.field_of(self.player.x, self.player.y)
        
        if self.land[pos[0]][pos[1]] > 2 and pressed[pyglet.window.key.ENTER]:
            self.houses[self.land[pos[0]][pos[1]] - 3].come_in(self)
        
        if self.land[pos[0]][pos[1]] == 2:
            if self.exit.acces(self.inventory):
                print("succesfuly done in {} seconds".format(self.timer))
                if self.id_level == "13":
                    return "LOST"
                return "EXIT"
                    
        #spells and attacks and items
        
        #spells
        
        succesful = [self.active_spells[x].active for x in range(len(self.active_spells))]
        
        for spell in self.active_spells:
            if not spell.active:
                spell.update(dt)
                
        #epellinventary
        
        self.spell_inventory.update(dt)
        
        #attacks
        
        for i, enemy in enumerate(self.enemies):
            position = utility.field_of(enemy.x, enemy.y)
            if utility.distance(self.player, enemy) <= 0:
                self.player.enemy_attack(enemy.data.attack, dt)
            
            for j, spell in enumerate(self.active_spells):
                if spell.active and spell.was_hit(enemy):
                    succesful[j] = True
        
        for i, succ in reversed([(x, succesful[x]) for x in range(0, len(succesful))]):
            if self.active_spells[i].active and succ:
                self.casted_spells.append([self.active_spells[i], 0.25])
                self.active_spells.pop(i)
        
        #casted spells
        
        for spell in self.casted_spells:
            spell[1] -= dt
        
        while len(self.casted_spells) > 0 and self.casted_spells[0][1] <= 0:
            utility.destroy(self.casted_spells[0][0])
            self.casted_spells.pop(0)
        
        #items
        
        collected = []
        for i, item in enumerate(self.active_items):
            position = utility.field_of(item.sprite.x, item.sprite.y)
            if self.land[int(position[0])][int(position[1])] == 0:
                x = int(position[0])
                y = int(position[1])
                
                if y + 1 < len(self.land[0]) and self.land[x][y + 1] == 1:
                    item.sprite.set_position(x * size + size // 2, (y + 1) * size + size // 2)
                elif y - 1 >= 0 and self.land[x][y - 1] == 1:
                    item.sprite.set_position(x * size + size // 2, (y - 1) * size + size // 2)
                elif x + 1 < len(self.land) and self.land[x + 1][y] == 1:
                    item.sprite.set_position((x + 1) * size + size // 2, y * size + size // 2)
                else:
                    item.sprite.set_position((x - 1) * size + size // 2, y * size + size // 2)
            if pos == position:
                if self.inventory.collect(item):
                    item.collect()
                    collected.append(i)
                
        for i in reversed(collected):
            self.active_items.pop(i)
        
        #keys (key events)
        
        for key, is_pressed in pressed.items():
            if is_pressed and key in D:
                self.player.move(dt, key)
            elif is_pressed and used[key] == False:
                self.inventory.move_pointer(key, self.player)
                self.spell_inventory.key_press( key)
                used[key] = True
        
        #move
        for enemy in self.enemies:
            enemy.move(dt)
            self.process_collision(enemy)
            
        self.player.update(dt)
        self.process_collision(self.player)
        
        to_destroy = []
        
        for i, enemy in enumerate(self.enemies):
            if enemy.is_dead(self.active_items):
                to_destroy.append(i)
        
        for i in reversed(to_destroy):
            self.enemies.pop(i)
    
    def click(self, x, y, button):
        if self.in_house != None:
            self.in_house.click(x, y, button, self)
        else:
            self.active_spells += self.spell_inventory.mouse_click(self.player, self.entities_batch, button)
    
    def replay(self):
        self.load()
