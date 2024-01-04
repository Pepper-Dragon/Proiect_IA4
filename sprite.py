import pygame
from pygame.transform import scale

import objutils as utils

from pygame.sprite import Group
from globals import *

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, groups, image = pygame.Surface((TILE_SIZE, TILE_SIZE)), position=(0, 0), size=(1, 1)):
        super().__init__(groups)
        self.image = image

        actual_position = (position[0] * TILE_SIZE, position[1] * TILE_SIZE)
        actual_size = (size[0] * TILE_SIZE, size[1] * TILE_SIZE)

        self.rect = self.image.get_rect(center=actual_position)

    def update(self):
        pass


