import pygame

import objutils as utils
from ball import Ball

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
        self.balls = []
        self.dynamic_objects = []
        self.sprites = Camera()
        # self.colliders = pygame.sprite.Group()

        # Player
        self.player = Player(app.screen, (100, 390), {})
        #self.player = Player(app.screen, (2300, 40), {})
        #self.player = Player(app.screen, (1000, 500), {})

        self.player.enlarge(2)

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

        max_step = 10
        i = 0

        while dt > 0.0:
            i += 1

            self.player.update()

            deltatime = min(dt, 0.0006)

            utils.euler_integ(self.player.ball, deltatime * 12)

            for obj in self.dynamic_objects:
                obj.forces()
                utils.euler_integ(obj, deltatime * 12)
                utils.colider(obj)
                utils.collision(self.player.ball, obj)
                utils.collision(obj, self.player.ball)

            utils.colider(self.player.ball)

            for obj in self.objects:
                utils.colider(obj)
                if utils.collision(self.player.ball, obj):
                    self.player.check_grounded(obj)

                for dynamic_obj in self.dynamic_objects:
                    utils.collision(dynamic_obj, obj)
                for ball in self.balls:
                    utils.collision(ball, obj)

            for dynamic_obj in self.dynamic_objects:
                for ball in self.balls:
                    utils.collision(dynamic_obj, ball)
                    utils.collision(ball, dynamic_obj)

                for dynamic_obj2 in self.dynamic_objects:
                    if dynamic_obj2 != dynamic_obj:
                        utils.collision(dynamic_obj, dynamic_obj2)
                        utils.collision(dynamic_obj2, dynamic_obj)

            for ball in self.balls:
                ball.forces()
                utils.euler_integ(ball, deltatime * 12)
                utils.colider(ball)
                if utils.sphere_collision(self.player.ball, ball):
                    self.player.enlarge(2)
                    self.balls.remove(ball)

            dt -= deltatime
            if i > max_step:
                break

    def draw(self):
        self.app.screen.fill('lightblue')
        self.sprites.draw(self.player, self.app.screen, self.balls, self.dynamic_objects)

    def create_level(self):
        # Floor
        for i in range(0, 14):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (i, 8), (1, 1), 1, (0, 0, 0), True))

        for i in range(0, 14):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (13+i, 17), (1, 1), 1, (0, 0, 0), True))

        for i in range(0, 11):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (26+i, 8), (1, 1), 1, (0, 0, 0), True))

        for i in range(0, 15):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (37+i, 4), (1, 1), 1, (0, 0, 0), True))

        # Walls
        for i in range(5, 8):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (0, i), (1, 1), 1, (0, 0, 0), True))

        for i in range(0, 8):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (13, 9+i), (1, 1), 1, (0, 0, 0), True))

        for i in range(0, 8):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (26, 9+i), (1, 1), 1, (0, 0, 0), True))

        for i in range(4, 8):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (36, i), (1, 1), 1, (0, 0, 0), True))

        for i in range(4, 8):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (29, i-3), (1, 1), 1, (0, 0, 0), True))

        self.objects.append(
            Rect([self.sprites], self.atlas_textures['platform_1_t'], (42, 1), (1, 1), 1, (0, 0, 0), True))

        for i in range(0, 2):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (52, 4-i), (1, 1), 1, (0, 0, 0), True))

        #Top Walls

        for i in range(0, 5):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (i, 5), (1, 1), 1, (0, 0, 0), True))

        for i in range(9, 30):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (i, 5), (1, 1), 1, (0, 0, 0), True))

        for i in range(5, 19):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (24 + i, 0), (1, 1), 1, (0, 0, 0), True))


        # Platforms
        for i in range(0, 6):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (4 + i, 6), (1, 1), 1, (0, 0, 0), True))

        for i in range(0, 2):
            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (18 + i, 14), (1, 1), 1, (0, 0, 0), True))

            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (22 + i, 12), (1, 1), 1, (0, 0, 0), True))

            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (18 + i, 14), (1, 1), 1, (0, 0, 0), True))

            self.objects.append(
                Rect([self.sprites], self.atlas_textures['platform_1_t'], (18 + i, 10), (1, 1), 1, (0, 0, 0), True))

            for i in range(5, 11):
                self.objects.append(
                    Rect([self.sprites], self.atlas_textures['platform_1_t'], (37 + i, 2), (1, 1), 1, (0, 0, 0), True))

        self.balls.append(Ball(750, 360, 10, 10, 2, (100, 0, 80)))
        #self.balls.append(Ball(800, 360, 10, 10, 2, (100, 0, 80)))

        self.balls.append(Ball(1230, 400, 10, 10, 2, (100, 0, 80)))
        self.balls.append(Ball(1400, 430, 10, 10, 2, (100, 0, 80)))
        self.balls.append(Ball(1200, 800, 10, 10, 2, (100, 0, 80)))

        self.balls.append(Ball(2800, 180, 6, 10, 1.1, (100, 0, 80)))

        self.dynamic_objects.append(
            Rect([self.sprites], self.atlas_textures['platform_1_t'], (32, 3), (0.2, 4), 1, (50, 20, 46), False))

        self.dynamic_objects.append(
            Rect([self.sprites], self.atlas_textures['platform_1_t'], (39, 2), (0.75, 0.75), 0.5, (50, 20, 46), False))
