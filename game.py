import pygame
import sys

from globals import *
from scene import Scene


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True

        self.scene = Scene(self)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

        self.close()

    def update(self):
        self.scene.update()

        pygame.display.update()
        self.clock.tick(FPS)

    def draw(self):
        self.scene.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def close(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
