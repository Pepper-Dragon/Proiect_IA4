import pygame

import objutils as utils

from camera import Camera
from deltaTime import DeltaTime
from sprite import GameSprite
from player import Player
from globals import *

from texturedata import atlas_texture_data
from rectangle import Rect


class Scene:
    def __init__(self, app) -> None:
        self.app = app

        self.atlas_textures = self.gen_atlas_textures('assets/Tiles/spritesheet.png')

        self.objects = []
        self.sprites = Camera()
        # self.colliders = pygame.sprite.Group()

        # Player
        self.player = Player(app.screen, (300, 360), {})

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
        dt = DeltaTime.getDeltaTime()

        while dt > 0:
            self.player.update()

            deltatime = min(dt, 0.0006)

            utils.euler_integ(self.player.ball, deltatime * 10)

            utils.colider(self.player.ball)

            for obj in self.objects:
                utils.colider(obj)
                if utils.collision(self.player.ball, obj):
                    self.player.check_grounded(obj)

            dt -= deltatime

    def draw(self):
        self.app.screen.fill('lightblue')
        self.sprites.draw(self.player, self.app.screen)
        # self.player.draw()

    def create_level(self):
        # Floor
        for i in range(0, 10):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (i, 8), (1, 1), 1, (0, 0, 0), True))

        # Walls
        for i in range(0, 8):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (0, i), (1, 1), 1, (0, 0, 0), True))
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (9, i), (1, 1), 1, (0, 0, 0), True))
