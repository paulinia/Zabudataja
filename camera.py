import pyglet
from pyglet.gl import *

class Camera:
    def __init__(self, width: float, height: float, position: list, zoom: float):
        self.width = float(width)
        self.height = float(height)
        self.position = list(position)
        self.zoom = float(zoom)

    def left(self):
        return self.position[0] - self.width / 2 / self.zoom

    def right(self):
        return self.position[0] + self.width / 2 / self.zoom

    def bottom(self):
        return self.position[1] - self.height / 2 / self.zoom

    def top(self):
        return self.position[1] + self.height / 2 / self.zoom

    def begin(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glPushMatrix()

        left = self.left()
        right = self.right()
        bottom = self.bottom()
        top = self.top()
        glOrtho(left, right, bottom, top, +1, -1)
    
    def end(self):
        glPopMatrix()
