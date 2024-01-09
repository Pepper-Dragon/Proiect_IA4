import pygame
import sys

from events import EventHandler
from globals import *
from scene import Scene
from deltaTime import DeltaTime


class Game:
    def __init__(self):
        pygame.init()

        EventHandler.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True

        self.scene = Scene(self)

        self.font = pygame.font.SysFont("Arial", 18, bold=True)

    def run(self):
        while self.running:
            DeltaTime.update()
            self.events()
            self.update()
            self.draw()

        self.close()

    def update(self):
        self.scene.update()

        pygame.display.update()
        self.clock.tick()

    def draw(self):
        self.scene.draw()
        self.show_fps()

    def events(self):
        EventHandler.poll_events()
        for event in EventHandler.events:
            if event.type == pygame.QUIT:
                self.running = False

    def close(self):
        pygame.quit()
        sys.exit()

    def show_fps(self):
        fps = "FPS: " + str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, 1, pygame.Color("coral"))
        self.screen.blit(fps_text, (SCREEN_WIDTH - 100, 10))

if __name__ == "__main__":
    game = Game()
    game.run()
