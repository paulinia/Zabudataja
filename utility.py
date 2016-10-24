from constants import *
from math import sqrt

mouse_x = 0
mouse_y = 0

def field_of(x, y):
    return (int(x // size), int(y // size))

def destroy(entity):
    entity.sprite.delete()
    
def process_collision(entity, position):
    move_up = position[1] * size + size - entity.y + entity.sprite.height // 2
    move_down = entity.y - (position[1] * size - entity.sprite.height // 2)
    move_right = position[0] * size + size - entity.x + entity.sprite.width // 2
    move_left = entity.x - (position[0] * size - entity.sprite.width // 2)
    if min(min(move_down, move_up), min(move_left, move_right)) == move_up:
        entity.y += move_up
        entity.sprite.set_position(entity.x, entity.y)
    elif min(min(move_down, move_up), min(move_left, move_right)) == move_down:
        entity.y -= move_down
        entity.sprite.set_position(entity.x, entity.y)
    elif min(min(move_down, move_up), min(move_left, move_right)) == move_right:
        entity.x += move_right
        entity.sprite.set_position(entity.x, entity.y)
    elif min(min(move_down, move_up), min(move_left, move_right)) == move_left:
        entity.x -= move_left
        entity.sprite.set_position(entity.x, entity.y)

def scale_sprite(entity, size_of):
    maximum = max(entity.image.height, entity.image.width)
    scale = size_of / maximum
    entity.sprite.scale = scale

def distance(B, A): # A, B are entities 
    dx = abs(A.x - B.x)
    dy = abs(A.y - B.y)
    
    size_A = min(A.sprite.width, A.sprite.height) / 2
    size_B = min(B.sprite.height, B.sprite.width) / 2
    
    return max(0, sqrt(dx * dx + dy * dy) - size_A - size_B)
    
def rotate_to_position(now, then):
    if now == then:
        return (0, 0)
    dx = then[0] - now[0] 
    dy = then[1] - now[1]
    return dx / sqrt(dx ** 2 + dy ** 2), dy / sqrt(dx ** 2 + dy ** 2)

def conventer(zoom, cx, cy, x, y):
    new_x = (cx - width / (2 * zoom)) + x / zoom
    new_y = cy - height / (2 * zoom) + y / zoom
    return new_x, new_y

def split(maxlen, message):
    new = ['']
    words = message.split()
    for word in words:
        if len(new[-1] + ' ' + word) > maxlen:
            new.append(word)
        else:
            new[-1] += " " + word
    
    return new

player_effects = pyglet.media.Player()
player_music = pyglet.media.Player()
