import pygame


class EventHandlerClass:
    # def __init__(self):
        # self.events = pygame.event.get()

    def init(self):
        self.events = pygame.event.get()

    def poll_events(self):
        self.events = pygame.event.get()

    def keydown(self, key):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return True
        return False


EventHandler = EventHandlerClass()

