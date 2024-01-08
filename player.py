import pygame.sprite

import objutils as utils

from events import EventHandler
from globals import *
from ball import Ball
from deltaTime import DeltaTime


class Player:
    def __init__(self, screen, position: tuple, parameters: dict):
        self.screen = screen
        self.ball = Ball(position[0], position[1], 10, 30, 1, (100, 0, 80))

    #     self.image = image
    #     self.image.fill('green')
    #     self.rect = self.image.get_rect(topleft=position)
    #
    #     # parameters
    #     self.colliders = parameters['colliders']
    #
    #     self.velocity = pygame.math.Vector2(0, 0)
    #     self.mass = 1
    #     self.term_vel = TERM_VEL
    #
        # is grounded ?
        self.is_grounded = False

    def input(self):
        if EventHandler.is_pressed(pygame.K_a):
            for point in self.ball.points:
                point.fx -= PLAYER_MOVE_FORCE

        if EventHandler.is_pressed(pygame.K_d):
            for point in self.ball.points:
                point.fx += PLAYER_MOVE_FORCE

        if EventHandler.keydown(pygame.K_w) and self.is_grounded:
            for point in self.ball.points:
                point.vy -= JUMP_VEL

    def move(self):
        pass

    def enlarge(self):
        self.ball.p += 2000

    def check_grounded(self, collider):
        if self.ball.collider.centery < collider.collider.centery:
            self.is_grounded = True

    def get_adjusted_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()

        player_offset = pygame.math.Vector2()
        player_offset.x = SCREEN_WIDTH / 2 - self.rect.centerx
        player_offset.y = SCREEN_HEIGHT / 2 - self.rect.centery

        return mouse_pos + player_offset

    def update(self):
        self.ball.forces()
        self.input()
        self.move()

        self.is_grounded = False

    def draw(self, offset):
        self.ball.draw(self.screen, offset)
