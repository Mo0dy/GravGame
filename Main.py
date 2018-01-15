from GravGame.Well import *
from GravGame.Light import *
from GravGame.Planet import *
from copy import deepcopy
import time


# Constants
# Window size
size_x = 800
size_y = 800
# background color
background = GREY

# Initializes pygame
pg.init()
# Creates a surface to draw onto
screen = pg.display.set_mode([size_x, size_y]) #, pg.FULLSCREEN | pg.HWSURFACE)
pg.display.set_caption("Gravity Well")


# stores the gravity wells
wells = []
# stores planets
planets = []


# draws on the screen
def draw():
    screen.fill(background)
    for w in wells:
        w.draw(screen)
    for p in planets:
        p.draw(screen)
    # Updates the screen
    pg.display.update()

planets = [CastPlanet(to_vec(400, 100), 30, GREEN, wells, planets, size_x, size_y),
            GoalPlanet(to_vec(400, 700), 20, GREEN)]

def setup():
    # sets rays global so it can be edited in this function
    global wells
    global rays
    global planets
    wells = [Well(400, 400, 80000000)]

    screen.fill(background)  # sets the whole screen to color background
    draw()


def my_exit(dt):
    global loop
    loop = False


def reset(dt):
    setup()


def create_well(dt):
    global wells
    wells.append(Well(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 80000000))
    for p in planets:
        if isinstance(p, CastPlanet):
            p.cast_ray(wells, planets, size_x, size_y)


precision = 0.001


def increase_precision(dt):
    global precision
    precision = precision / 10
    print(precision)


def decrease_precision(dt):
    global precision
    precision *= 10
    print(precision)


def move_little_left(dt):
    global planets
    for p in planets:
        if isinstance(p, CastPlanet):
            p.aim += precision
            p.cast_ray(wells, planets, size_x, size_y)

def move_little_right(dt):
    global planets
    for p in planets:
        if isinstance(p, CastPlanet):
            p.aim -= precision
            p.cast_ray(wells, planets, size_x, size_y)


keypressed_functions = {
    pg.K_ESCAPE: my_exit,
    pg.K_SPACE: reset,
    pg.K_RIGHT: move_little_right,
    pg.K_LEFT: move_little_left,
}


keydown_functions = {
    pg.K_c: create_well,
    pg.K_o: increase_precision,
    pg.K_l: decrease_precision,
}

keydown = []  # stores the keys that were pressed each turn
keyup = []  # stores the keys that were released each turn
keypressed = {}  # stores if key is currently pressed

#  Updates everything in the game. This is the main place for gamelogic
def update(dt):
    global keydown
    global keyup
    global rays
    for s in selection:
        if isinstance(s, Planet):
            s.point_at(pg.mouse.get_pos())
            s.cast_ray(wells, planets, size_x, size_y)
        elif isinstance(s, Well):
            s.set_size(length(s.pos - pg.mouse.get_pos()) / 4)
            for p in planets:
                if isinstance(p, CastPlanet):
                    p.cast_ray(wells, planets, size_x, size_y)
    for k in keypressed:

        if keypressed[k]:
            try:
                keypressed_functions[k](dt)
            except:
                pass
        for k in keydown:
            try:
                keydown_functions[k](dt)
            except:
                pass
    keydown = []
    keyup = []
    #   l.update(dt, wells)


def keyhandler():
    global keydown
    global keyup

    for k in keydown:
        keypressed[k] = True
    for k in keyup:
        keypressed[k] = False


selection = []
def on_click():
    pos = pg.mouse.get_pos()
    for p in planets:
        if is_on(pos, p):
            selection.append(p)
    for w in wells:
        if is_on(pos, w):
            selection.append(w)



def on_release():
    global selection
    selection = []


setup()
# input()
old_time = time.time()  # to calculate dt
loop = True  # this is here so i can stop the loop
while loop:
    # calculate dt
    curr_time = time.time()
    dt = curr_time - old_time
    # dt = dt * 10
    old_time = curr_time

    # event handling
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False  # the loop will end
        # saves what keys were pressed / released
        elif e.type == pg.KEYDOWN:
            keydown.append(e.key)
        elif e.type == pg.KEYUP:
            keyup.append(e.key)
        elif e.type == pg.MOUSEBUTTONDOWN:
            on_click()
        elif e.type == pg.MOUSEBUTTONUP:
            on_release()

    keyhandler()
    update(dt)
    # collision(rays, wells)
    # out_of_bounds(rays, 0, size_x, 0, size_y)
    draw()

pg.quit()


