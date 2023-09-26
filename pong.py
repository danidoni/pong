from typing import List
from math import sin, cos, radians

# import basic pygame modules
import pygame as pg

SCREENRECT = pg.Rect(0, 0, 640, 480)
PADDLE_SIZE = (10, 100)
BALL_SIZE = (10, 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Paddle:
    def __init__(self, position):
        self.score = 0
        self.rect = pg.Rect(position, PADDLE_SIZE)

    def render(self, pg, screen):
        pg.draw.rect(screen, WHITE, self.rect)

    def move_up(self):
        if self.rect.top - 5 >= 0:
            self.rect.move_ip(0, -5)

    def move_down(self):
        if self.rect.bottom + 5 <= SCREENRECT.bottom:
            self.rect.move_ip(0, 5)

    def score_up(self):
        self.score += 1


class Ball:
    def __init__(self, position: pg.Vector2, speed, angle) -> None:
        self.speed = speed
        # In degrees, 0 is down, 90 to the right
        self.angle = angle
        self.position: pg.Vector2 = position

    def velocity(self) -> pg.Vector2:
        rads = radians(self.angle)
        x = sin(rads) * self.speed
        y = cos(rads) * self.speed
        return pg.Vector2(x, y)

    def rect(self) -> pg.Rect:
        return pg.Rect(self.position, BALL_SIZE)

    def render(self, pg, screen):
        pg.draw.rect(screen, WHITE, self.rect())

    def update(self):
        next_position = self.position + self.velocity()
        if next_position.x <= 0:
            # That means the angle is between 180 and 360, for example 190, to bounce it has to become 90, 
            # so 180 - angle - 180 = -angle
            self.angle *= -1 # 180 - self.angle - 180
        if next_position.x + BALL_SIZE[0] >= SCREENRECT[2]:
            # That means the angle is between 0 and 180, for example 100, to bounce it has to become 260
            # -angle as well
            self.angle *= -1
        if next_position.y <= 0:
            # That means the angle is between 90 and 270, for example 100, to bounce it has to become 80
            # 90 - angle + 90 = 
            self.angle = 180 - self.angle
        if next_position.y + BALL_SIZE[1] >= SCREENRECT[3]:
            # That means the angle is between 270 and 90, for example 30, to bounce it has to become 150
            # 90 - angle + 90 = 
            self.angle = 180 - self.angle

        self.position = next_position


class CollisionSystem:
    def update(self, ball, player_paddle, ai_paddle):
        ball_rect = ball.rect()
        if ball_rect.colliderect(player_paddle.rect):
            ball.angle *= -1

        if ball_rect.colliderect(ai_paddle.rect):
            ball.angle *= -1


class ScoreSystem:
    def update(self, ball, player_paddle, ai_paddle):
        if ball.position.x <= 0:
            ai_paddle.score_up()

        if ball.position.x + BALL_SIZE[0] >= SCREENRECT[2]:
            player_paddle.score_up()

        print("Player: ", player_paddle.score, " AI: ", ai_paddle.score)


def main(winstyle=0):
    # Initialize pygame
    pg.init()

    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    pg.display.set_caption("Pong")

    my_font = pg.freetype.SysFont('Monospace', 30)
    text_surface = my_font.render('Some Text', False, (220, 0, 0))

    player_paddle = Paddle((10, (SCREENRECT[3] / 2) - (PADDLE_SIZE[1] / 2)))
    other_paddle = Paddle((SCREENRECT[2] - 20, (SCREENRECT[3] / 2) - (PADDLE_SIZE[1] / 2)))
    ball = Ball(position=pg.Vector2(x=SCREENRECT[2] / 2 - BALL_SIZE[0] / 2, y= SCREENRECT[3] / 2 - BALL_SIZE[1] / 2),
                speed=5,
                angle=100)

    collision_system = CollisionSystem()
    score_system = ScoreSystem()

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

        collision_system.update(ball, player_paddle, other_paddle)
        score_system.update(ball, player_paddle, other_paddle)

        screen.fill(BLACK)

        player_paddle.render(pg, screen)
        other_paddle.render(pg, screen)
        ball.render(pg, screen)

        text_surface, _ = my_font.render(str(player_paddle.score), (255, 255, 255))
        screen.blit(text_surface, (0, 0))

        text_surface, _ = my_font.render(str(other_paddle.score), (255, 255, 255))
        screen.blit(text_surface, (SCREENRECT[2] - 20, 0))

        pg.display.update()

        clock.tick(40)

# call the "main" function if running this script
if __name__ == "__main__":
    main()
    pg.quit()