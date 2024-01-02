import pygame
import sys

from globals import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

        self.close()

    def update(self):
        pygame.display.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill('lightblue')

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
