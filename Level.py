from GravGame.Game import *
from GravGame.Planet import *
from GravGame.Well import *


# this holds the information for a level
class Level(object):
    def __init__(self, wells, planets):
        self.wells = wells
        self.planets = planets


# a list of the different levels. These should probably be saved in files that are able to be edited in a level editor
# mode
levels = {
    "test_level": Level(
        [[Well(400, 400, 80000000)],
         [CastPlanet(to_vec(400, 100), 30, GREEN),
          GoalPlanet(to_vec(400, 700), 20, GREEN)]]
    )
}