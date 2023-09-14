import os
import random
from typing import List

# import basic pygame modules
import pygame as pg

SCREENRECT = pg.Rect(0, 0, 640, 480)
PADDLE_SIZE = (10, 100)

class Paddle:
    def __init__(self, position, size, color):
        self.position = position
        self.size = size
        self.color = color

    def render(self, pg, screen):
        rect = pg.Rect(self.position, self.size)
        pg.draw.rect(screen, self.color, rect)

def main(winstyle=0):
    # Initialize pygame
    pg.init()

    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    pg.display.set_caption("Pong")

    player_paddle = Paddle((10, (SCREENRECT[3] / 2) - (PADDLE_SIZE[1] / 2)), PADDLE_SIZE, (255, 255, 255))
    other_paddle = Paddle((SCREENRECT[2] - 20, (SCREENRECT[3] / 2) - (PADDLE_SIZE[1] / 2)), PADDLE_SIZE, (255, 255, 255))

    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return

        player_paddle.render(pg, screen)
        other_paddle.render(pg, screen)

        pg.display.update()

        clock.tick(40)

# call the "main" function if running this script
if __name__ == "__main__":
    main()
    pg.quit()