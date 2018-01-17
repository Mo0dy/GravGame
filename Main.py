from GravGame.Game import *
from GravGame.KeyHandler import *
from GravGame.Level import *
import time

pg.init()
game = Game()
init_levels(game)

key_handlers = {
    "main": Keyhandler(game,
        pressed_functions={
            pg.K_ESCAPE: game.my_exit,
            pg.K_SPACE: game.reset,
            pg.K_RIGHT: game.move_little_right,
            pg.K_LEFT: game.move_little_left,
        },
        pushed_functions={
            pg.K_c: game.create_well,
            pg.K_DOWN: game.increase_precision,
            pg.K_UP: game.decrease_precision,
        }
    )
}

key_handler = key_handlers["main"]

game.setup()
loop = True
old_time = time.time()

while loop:
    # calculate dt
    current_time = time.time()
    dt = current_time - old_time
    old_time = current_time

    # event handling
    keys_pushed = []
    keys_released = []
    mouse_down = False
    mouse_up = False
    for e in pg.event.get():
        if e.type == pg.QUIT:
            loop = False  # the loop will end
        # saves what keys were pressed / released
        elif e.type == pg.KEYDOWN:
            keys_pushed.append(e.key)
        elif e.type == pg.KEYUP:
            keys_released.append(e.key)
        elif e.type == pg.MOUSEBUTTONDOWN:
            mouse_down = True
        elif e.type == pg.MOUSEBUTTONUP:
            mouse_up = True
    key_handler.handle_input(keys_pushed, keys_released, mouse_down, mouse_up, dt)
    game.update(dt)
    game.draw()
