import pygame

from sprite import GameSprite
from player import Player
from globals import *
from texturedata import atlas_texture_data


class Scene:
    def __init__(self, app) -> None:
        self.app = app

        self.atlas_textures = self.gen_atlas_textures('assets/Tiles/spritesheet.png')

        self.sprites = pygame.sprite.Group()
        self.gameSprite = GameSprite([self.sprites], image=self.atlas_textures['platform_1_t'])
        GameSprite([self.sprites], position=(100, 100))
        GameSprite([self.sprites], position=(200, 200))

        self.player = Player([self.sprites], pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 3)), (600, 100), {})

    def gen_atlas_textures(self, filepath):
        textures = {}

        atlas_img = pygame.transform.scale(pygame.image.load(filepath).convert_alpha(),
                                           (TILE_SIZE * ATLAS_COLS, TILE_SIZE * ATLAS_ROWS))

        for name, data in atlas_texture_data.items():
            textures[name] = atlas_img.subsurface(
                pygame.Rect(data['position'][0] * TILE_SIZE, data['position'][1] * TILE_SIZE, data['size'][0],
                            data['size'][1]))

        return textures

    def update(self):
        self.sprites.update()

    def draw(self):
        self.app.screen.fill('lightblue')
        self.sprites.draw(self.app.screen)
