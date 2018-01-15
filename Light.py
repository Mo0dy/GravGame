from GravGame.Utility import *
from copy import deepcopy

LIGHTSPEED = 1000
RAY_STEPSIZE = 0.005


class Ray(GameObj):
    def __init__(self, pos, vel, color, wells, planets, p, min_x, max_x, min_y, max_y):
        super().__init__(pos, 2, color)
        self.vel = vel / length(vel) *  LIGHTSPEED
        self.tail = []
        self.create(wells, planets, p, min_x, max_x, min_y, max_y)

    def create(self, wells, planets, p, min_x, max_x, min_y, max_y):
        pos = self.pos
        vel = self.vel
        forces = np.zeros(2)
        while pos[0] > min_x and pos[0] < max_x and pos[1] > min_y and pos[1] < max_y and not self.collision(wells, planets, p):
            # out of bounds and wells collision
            self.tail.append(deepcopy(pos))
            # Update Velocity then update position
            for w in wells:
                c_vec = w.pos - self.pos
                distance = length(c_vec)
                forces += w.m / distance ** 4 * c_vec  # / distance ** 3 would be more correct but / distance ** 4 is more fun
            vel += forces * RAY_STEPSIZE
            vel = vel / np.sqrt(np.dot(vel, vel)) * LIGHTSPEED
            pos += vel * RAY_STEPSIZE

    def collision(self, wells, planets, p):
        for w in wells:
            c_vec = w.pos - self.pos
            if np.dot(c_vec, c_vec) < np.square(w.size):
                return True
        for plan in planets:
            if not plan == p:
                c_vec = plan.pos - self.pos
                if np.dot(c_vec, c_vec) < np.square(plan.size):
                    if plan.color == p.color:
                        self.planet = plan
                        plan.connected = True
                        p.connected = True
                    return True
        return False

    def draw(self, screen, mat=mat_identity()):
        super().draw_child(screen, mat)
        for i in range(len(self.tail) - 1):
            pg.draw.aaline(screen, self.color, translate(self.tail[i], mat), translate(self.tail[i + 1], mat), self.size * 2)