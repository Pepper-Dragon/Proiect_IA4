import pygame

from pygame.sprite import Group
from globals import *

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, groups, image = pygame.Surface((TILE_SIZE, TILE_SIZE)), position=(0, 0)):
        super().__init__(groups)
        self.image = image

        actual_position = (position[0] * TILE_SIZE, position[1] * TILE_SIZE)

        self.rect = self.image.get_rect(topleft=actual_position)

    def update(self):
        pass
        # self.rect.x += 1


