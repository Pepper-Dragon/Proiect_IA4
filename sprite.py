import pygame

from pygame.sprite import Group
from globals import *

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, groups, image = pygame.Surface((TILE_SIZE, TILE_SIZE)), position = (0, 0)):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = position)

    def update(self):
        pass
        # self.rect.x += 1


