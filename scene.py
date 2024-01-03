import pygame

from camera import Camera
from sprite import GameSprite
from player import Player
from globals import *
from texturedata import atlas_texture_data


class Scene:
    def __init__(self, app) -> None:
        self.app = app

        self.atlas_textures = self.gen_atlas_textures('assets/Tiles/spritesheet.png')

        self.sprites = Camera()
        self.colliders = pygame.sprite.Group()

        self.gameSprite = GameSprite([self.sprites], image=self.atlas_textures['platform_1_t'])
        GameSprite([self.sprites], position=(100, 100))
        GameSprite([self.sprites], position=(200, 200))

        # Floor
        GameSprite([self.sprites, self.colliders], pygame.Surface((TILE_SIZE * 14, TILE_SIZE * 1)), (200, 500))

        # Player
        self.player = Player([self.sprites], pygame.Surface((TILE_SIZE * 1, TILE_SIZE * 2)), (400, 300), {'colliders': self.colliders})

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
        self.sprites.draw(self.player, self.app.screen)
