import os
import random
from typing import List

# import basic pygame modules
import pygame as pg

SCREENRECT = pg.Rect(0, 0, 640, 480)
PADDLE_SIZE = (10, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Paddle:
    def __init__(self, position):
        self.rect = pg.Rect(position, PADDLE_SIZE)

    def render(self, pg, screen):
        pg.draw.rect(screen, WHITE, self.rect)

    def move_up(self):
        if self.rect.top - 5 >= 0:
            self.rect.move_ip(0, -5)

    def move_down(self):
        if self.rect.bottom + 5 <= SCREENRECT.bottom:
            self.rect.move_ip(0, 5)

def main(winstyle=0):
    # Initialize pygame
    pg.init()

    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    pg.display.set_caption("Pong")

    player_paddle = Paddle((10, (SCREENRECT[3] / 2) - (PADDLE_SIZE[1] / 2)))
    other_paddle = Paddle((SCREENRECT[2] - 20, (SCREENRECT[3] / 2) - (PADDLE_SIZE[1] / 2)))

    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            
        if pg.key.get_pressed()[pg.K_w]:
            player_paddle.move_up()
        if pg.key.get_pressed()[pg.K_s]:
            player_paddle.move_down()

        screen.fill(BLACK)

        player_paddle.render(pg, screen)
        other_paddle.render(pg, screen)

        pg.display.update()

        clock.tick(40)

# call the "main" function if running this script
if __name__ == "__main__":
    main()
    pg.quit()