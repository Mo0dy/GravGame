from GravGame.Game import *
import time


game = Game()
game.setup()
loop = True
old_time = time.time()

while loop:
    current_time = time.time()
    dt = current_time - old_time
    old_time = current_time

    game.update(dt)
    game.draw()
