from GravGame.Utility import *
from pygame import gfxdraw


class Well(GameObj):
    def __init__(self, x, y, m=40000000, p=2000000):
        super().__init__(to_vec(x, y), 1, BLACK)
        self.m = m  # mass of object
        self.p = p  # density of object
        self.area = m / p

    def set_mass(self, mass):
        self.m = mass
        self.area = self.m / self.p

    def set_size(self, size):
        self.size = int(size)
        self.m = self.area * self.p

    @property
    def area(self):
        return np.pi * np.square(self.size) / 4

    @area.setter
    def area(self, other):
        self.size = int(np.sqrt(other / np.pi * 4))