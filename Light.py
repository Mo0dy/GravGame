from GravGame.Utility import *
import copy
import pygame as pg
import time

LIGHTSPEED = 1000
RAY_STEPSIZE = 0.005


class Ray(GameObj):
    def __init__(self, parent_planet, game):
        super().__init__(copy.copy(parent_planet.pos), 2, parent_planet.color.correct_gamma(1.5))
        self.tail = []
        self.game = game
        self.create(parent_planet)

    def create(self, parent_planet):
        pos = self.pos
        vel = vec_from_angle(parent_planet.aim) * LIGHTSPEED
        # out of bounds and collision check
        while pos[0] > 0 and pos[0] < self.game.size[0] and pos[1] > 0 and pos[1] < self.game.size[1] and not self.collision(parent_planet):
            # out of bounds and wells collision
            self.tail.append(copy.copy(pos))
            # Update Velocity then update position
            forces = np.zeros(2)
            for w in self.game.wells:
                c_vec = w.pos - self.pos
                distance = length(c_vec)
                forces += w.m * 2 / distance ** 4 * c_vec  # / distance ** 3 would be more correct but / distance ** 4 is more fun
            vel += forces * RAY_STEPSIZE
            vel = vel / np.sqrt(np.dot(vel, vel)) * LIGHTSPEED
            pos += vel * RAY_STEPSIZE


    def collision(self, parent_planet):
        for w in self.game.wells:
            c_vec = w.pos - self.pos
            if np.dot(c_vec, c_vec) < np.square(w.size):
                return True
        for plan in self.game.planets:
            if not plan == parent_planet:
                c_vec = plan.pos - self.pos
                if np.dot(c_vec, c_vec) < np.square(plan.size):
                    if plan.color == parent_planet.color:
                        self.planet = plan
                        plan.connected = True
                        parent_planet.connected = True
                    return True
        return False

    def draw(self, screen, mat=mat_identity()):
        super().draw_child(screen, mat)
        for i in range(len(self.tail) - 1):
            pg.draw.aaline(screen, self.color, translate(self.tail[i], mat), translate(self.tail[i + 1], mat), self.size * 2)