import numpy as np
import pygame as pg
from GravGame.Utility import *
from GravGame.Light import *
from GravGame.Planet import *
from GravGame.Well import *
from GravGame.Level import *


# This class contains everything important to the game
class Game(object):
    def __init__(self, size_x=800, size_y=800):
        # These lists hold the objects that act in the game
        self.planets = []
        self.wells = []

        # These are some "constants"
        # The size of the window
        self.size = [size_x, size_y]
        self.background = GREY
        # initializes the engine
        pg.init()
        # creates a screen to draw on
        self.screen = pg.display.set_mode(self.size)
        pg.display.set_caption("GravGame")

        # Some parameters that save the state of the game
        # Used to decide if program should end
        self.loop = True
        # Used to aim with the selected planets:
        self.precision = 0.001

    def draw(self):
        self.screen.fill(self.b)
        # draws all entities (light rays are stored in the planets and also get drawn there)
        for e in self.wells + self.planets:
            e.draw(self.screen)  # it is also possible to pass a transformation matrix here
        # Updates the screen
        pg.display.update()

    def update(self, dt):
        for p in self.planets:
            if isinstance(p, CastPlanet):
                p.cast_ray(self.wells, self.planets, self.size[0], self.size[1])

        # if it returns False the program should end
        return self.loop

    def setup(self):
        self.load_level("test_level")
        # Used to aim with the selected planets:
        self.precision = 0.001

    def load_level(self, name):
        level = levels[name]
        self.wells = level.wells
        self.planets = level.planets

    # Somewhat key functions. i.e. these will probably get called by the key handler
    def my_exit(self):
        loop = False

    def reset(self):
        self.setup()

    def create_well(self):
        self.wells.append(Well(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 80000000))

    # These functions are used to aim
    def increase_precision(self):
        self.precision /= 10

    def decrease_precision(self):
        self.precision *= 10

    def move_little_left(self, dt):
        # maybe i should store cast and goal planets seperately
        for p in self.planets:
            if isinstance(p, CastPlanet):
                # this should only work on a selected entitiy
                p.aim += self.precision * dt

    def move_little_right(self, dt):
        for p in self.planets:
            if isinstance(p, CastPlanet):
                p.aim -= self.precision * dt