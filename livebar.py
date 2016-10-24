from constants import *
import random

class Livebar:
    def __init__(self, maxlives, color = (0, 255, 0)):
        self.maxi = maxlives
        self.curent = maxlives
        self.color = color
    
    def set_lives(self, new_lives):
        self.curent = new_lives
    
    def draw(self, x, y):
        lenght = size
        thick = 5
        border = self.curent / self.maxi * lenght
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x - size // 2, y + size // 2, x - size // 2 + border, y + size // 2, 
                                                      x - size // 2 + border, y + size // 2 + thick, x - size // 2, y + size // 2 + thick)),
                                                     ('c3B', self.color * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x - size // 2 + border, y + size // 2, x - size // 2 + lenght, y + size // 2,
                                                             x - size // 2 + lenght, y + size // 2 + thick, x - size // 2 + border, y + size // 2 + thick)),
                                                            ('c3B', (255, 0, 0) * 4))
