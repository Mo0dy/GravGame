import pygame as pg
import numpy as np
from GravGame.Utility import *
from GravGame.Game import *


# this class handles the keyinput every update it gets passed the pressed and released keys
class Keyhandler(object):
    def __init__(self, game, **kwargs):
        self.game = game
        # this rememberes what keys are currently pressed
        self.pressed_keys = []
        # remembers mouse state
        self.mouse_pressed = False
        # these functions get called for the released keys
        if "released_functions" in kwargs:
            self.released_functions = kwargs["released_functions"]
        else:
            self.released_functions = {}
        # these functions get called for the pushed keys
        if "pushed_functions" in kwargs:
            self.pushed_functions = kwargs["pushed_functions"]
        else:
            self.pushed_functions = {}
        # these functions get called fot the currently pressed keys they will get called with dt
        if "pressed_functions" in kwargs:
            self.pressed_functions = kwargs["pressed_functions"]
        else:
            self.pressed_functions = {}

    def handle_input(self, keys_pushed, keys_released, mouse_down, mouse_up, dt=0):
        # updates the pressed keys: (maybe this should be solved with a dictionary)
        for k in keys_pushed:
            self.pressed_keys.append(k)
        for k in keys_released:
            self.pressed_keys.remove(k)

        # this called the mapped functions. The for loops could be integrated with the one above
        for k in keys_pushed:
            try:
                self.pushed_functions[k]()
            except:
                pass

        for k in keys_released:
            try:
                self.released_functions[k]()
            except:
                pass

        for k in self.pressed_keys:
            try:
                self.pressed_functions[k](dt)
            except:
                pass

        # mouse handling
        if mouse_down:
            self.mouse_pressed = True
            self.game.mouse_down()
        if mouse_up:
            self.mouse_pressed = False
            self.game.mouse_up()
        if self.mouse_pressed:
            self.game.mouse_pressed(dt)
