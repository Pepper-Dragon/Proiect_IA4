import pygame.sprite

from events import EventHandler
from globals import *


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, image: pygame.Surface, position: tuple, parameters: dict):
        super().__init__(groups)
        self.image = image
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=position)

        # parameters
        self.colliders = parameters['colliders']

        self.velocity = pygame.math.Vector2(0, 0)
        self.mass = 1
        self.term_vel = TERM_VEL

    #     is grounded ?
        self.is_grounded = False

    def input(self):
        self.velocity.x = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.velocity.x = -5

        if keys[pygame.K_d]:
            self.velocity.x = 5

    #     jumping
        if self.is_grounded and EventHandler.keydown(pygame.K_SPACE):
            self.velocity.y = -JUMP_VEL


    def move(self):
        self.velocity.y += GRAVITY * self.mass

        # Terminal velocity
        if self.velocity.y > self.term_vel:
            self.velocity.y = self.term_vel

        self.rect.x += self.velocity.x
        self.check_collisions('horizontal')
        self.rect.y += self.velocity.y
        self.check_collisions('vertical')

    def check_collisions(self, direction):
        if direction == 'horizontal':
            for collider in self.colliders:
                if self.rect.colliderect(collider.rect):
                    if self.velocity.x > 0:
                        self.rect.right = collider.rect.left
                    if self.velocity.x < 0:
                        self.rect.left = collider.rect.right
        elif direction == 'vertical':
            self.is_grounded = False

            for collider in self.colliders:
                if self.rect.colliderect(collider.rect):
                    if self.velocity.y >= 0:
                        self.rect.bottom = collider.rect.top
                        self.velocity.y = 0
                    if self.velocity.y < 0:
                        self.rect.top = collider.rect.bottom
                        self.velocity.y = 0

                # check if is grounded
                if not self.is_grounded and collider.rect.collidepoint(self.rect.centerx, self.rect.bottom + 1):
                    self.is_grounded = True

    def get_adjusted_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()

        player_offset = pygame.math.Vector2()
        player_offset.x = SCREEN_WIDTH / 2 - self.rect.centerx
        player_offset.y = SCREEN_HEIGHT / 2 - self.rect.centery

        return mouse_pos + player_offset

    def update(self):
        self.input()
        self.move()