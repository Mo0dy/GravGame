from GravGame.Utility import *
from GravGame.Light import *
import pygame as pg
from copy import deepcopy


class Planet(GameObj):
    def __init__(self, pos, size, color):
        super().__init__(pos, size, color)
        self.connected = False

    def draw(self, screen, mat=mat_identity()):
        if self.connected:
            color = self.color.correct_gamma(0.5)
        else:
            color = self.color
        self.draw_child(screen, mat)  # child draw function
        drawpos = to_tuple(translate(self.pos, mat))
        gfxdraw.aacircle(screen, drawpos[0], drawpos[1], self.size, color)
        gfxdraw.filled_circle(screen, drawpos[0], drawpos[1], self.size, color)


class CastPlanet(Planet):
    def __init__(self, pos, size, color, wells, planets, size_x, size_y):
        super().__init__(pos, size, color)
        self.aim = 0  # angle at which the Planet aims
        self.cast_ray(wells, planets, size_x, size_y)

    def draw_child(self, screen, mat):
        # draws aim vector
        self.ray.draw(screen, mat)
        pg.draw.aaline(screen, self.color.correct_gamma(2), self.pos, self.pos + translate(to_vec(100, 0), mat_rot(self.aim)), 3)

    def point_at(self, pos):
        c_vec = pos - self.pos
        angle = np.arccos(c_vec[0] / np.sqrt(np.dot(c_vec, c_vec)))
        if c_vec[1] > 0:
            self.aim = angle
        else:
            self.aim = -angle

    def cast_ray(self, wells, planets, size_x, size_y):
        self.connected = False
        try:
            self.ray.planet.connected = False
        except:
            pass
        self.ray = Ray(deepcopy(self.pos),
            translate(to_vec(LIGHTSPEED, 0), mat_rot(self.aim)),
            self.color.correct_gamma(0.5),
            wells, planets, self, 0, size_x, 0, size_y)


class GoalPlanet(Planet):
    def __init__(self, pos, size, color):
        super().__init__(pos, size, color)
