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

        # Player
        self.player = Player([self.sprites], pygame.Surface((TILE_SIZE, TILE_SIZE)), (300, 360),
                             {'colliders': self.colliders})

        self.create_level()

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

    def create_level(self):
        # Floor
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(7, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(8, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(9, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(10, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(11, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(12, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(13, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(14, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(15, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(16, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(17, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(18, 13))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(19, 13))

        #         Left wall
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(7, 12))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(7, 11))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(7, 10))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(7, 9))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(7, 8))

        #         Right wall
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(19, 12))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(19, 11))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(19, 10))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(19, 9))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(19, 8))

        #         Middle platform
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(13, 10))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(14, 10))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(15, 10))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(16, 10))
        GameSprite([self.sprites, self.colliders], image=self.atlas_textures['platform_1_t'], position=(17, 10))
