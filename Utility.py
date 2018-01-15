import numpy as np
import pygame as pg
from pygame import gfxdraw

# Color Values
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (15, 137, 51)
BLUE = (0, 0, 255)
GREY = (100, 100, 100)


# returns a linear interpolation from r1 to r2 at r with respect to v1 and v2
# this is used to set the color of the rays
def interpolate(r, r1, r2, v1, v2):
    return (v2 - v1) / (r2 - r1) * (r - r1) + v1


# checks if two circular object touch
def is_touching(obj1, obj2):
    return dist(obj1.pos, obj2.pos) < obj1.size + obj2.size


def is_on(pos, obj):
    return dist(pos, obj.pos) < obj.size


# checks the color at a pixel position
def is_color(screen, pos, color):
    pos = np.int(pos)
    return pg.surfarray.pixels3d()[pos[0], pos[1]] == color


# Vectors
# tuple from numpy array
def to_tuple(arr):
    return tuple(int(i) for i in arr)


# 3x3 identity mat. i.e. ones on diagonal
def mat_identity():
    return np.identity(3)


def mat_rot(angle):
    return np.array([[np.cos(angle), -np.sin(angle), 0],
                     [np.sin(angle), np.cos(angle), 0],
                     [0,                0,          1]])


def mat_trans(x, y):
    return np.array([[1, 0, x],
                     [0, 1, y],
                     [0, 0, 1]])


def mat_scale(sx, sy):
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]])

# distance between two points
def dist(pos1, pos2):
    c_vec = pos2 - pos1
    return np.sqrt(np.dot(c_vec, c_vec))


# returns the length of a vector
def length(vec):
    return np.sqrt(np.dot(vec, vec))


# creates a numpy array from two values
def to_vec(x, y):
    return np.array([x, y], dtype=float)


# translates a vector by multiplying it with a translation matrix
def translate(vec, mat):
    return np.dot(mat, np.append(vec, 1))[:2]


# basic game object that has a position, size and color:
class GameObj(object):
    def __init__(self, pos, size, color=(255, 255, 255)):
        self.size = int(size)
        self.pos = pos
        self.color = pg.Color(color[0], color[1], color[2])


    # overwritten for anti aliasing
    def draw(self, screen, mat=mat_identity()):
        self.draw_child(screen, mat)  # child draw function
        drawpos = to_tuple(translate(self.pos, mat))
        gfxdraw.aacircle(screen, drawpos[0], drawpos[1], self.size, self.color)
        gfxdraw.filled_circle(screen, drawpos[0], drawpos[1], self.size, self.color)

    def draw_child(self, screen, mat):
        pass

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, other):
        self.pos[0] = other

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, other):
        self.pos[1] = other
