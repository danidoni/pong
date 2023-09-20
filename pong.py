import os
import random
from typing import List

# import basic pygame modules
import pygame as pg

SCREENRECT = pg.Rect(0, 0, 640, 480)
PADDLE_SIZE = (10, 100)
BALL_SIZE = (10, 10)
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


class Ball:
    def __init__(self, position: pg.Vector2, velocity: pg.Vector2) -> None:
        self.position: pg.Vector2 = position
        self.velocity: pg.Vector2 = velocity

    def render(self, pg, screen):
        rect = pg.Rect(self.position, BALL_SIZE)
        pg.draw.rect(screen, WHITE, rect)

    def update(self):
        next_position = self.position + self.velocity
        if next_position.x <= 0:
            self.velocity.x *= -1
        if next_position.x + BALL_SIZE[0] >= SCREENRECT[2]:
            self.velocity.x *= -1
        if next_position.y <= 0:
            self.velocity.y *= -1
        if next_position.y + BALL_SIZE[1] >= SCREENRECT[3]:
            self.velocity.y *= -1

        self.position = next_position


def main(winstyle=0):
    # Initialize pygame
    pg.init()

    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    pg.display.set_caption("Pong")

    player_paddle = Paddle((10, (SCREENRECT[3] / 2) - (PADDLE_SIZE[1] / 2)))
    other_paddle = Paddle((SCREENRECT[2] - 20, (SCREENRECT[3] / 2) - (PADDLE_SIZE[1] / 2)))
    ball = Ball(position=pg.Vector2(x=SCREENRECT[2] / 2 - BALL_SIZE[0] / 2, y= SCREENRECT[3] / 2 - BALL_SIZE[1] / 2),
                velocity=pg.Vector2(-5, -5))

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

        ball.update()

        screen.fill(BLACK)

        player_paddle.render(pg, screen)
        other_paddle.render(pg, screen)
        ball.render(pg, screen)

        pg.display.update()

        clock.tick(40)

# call the "main" function if running this script
if __name__ == "__main__":
    main()
    pg.quit()