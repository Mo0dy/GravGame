import numpy as np
import pygame as pg
from GravGame.Utility import *
from GravGame.Light import *
from GravGame.Planet import *
from GravGame.Well import *


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

    def draw(self):
        self.screen.fill(self.b)
        # draws all entities (light rays are stored in the planets and also get drawn there)
        for e in self.wells + self.planets:
            e.draw(self.screen)  # it is also possible to pass a transformation matrix here
        # Updates the screen
        pg.display.update()

    def update(self, dt):
        pass