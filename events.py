import pygame


class EventHandlerClass:
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

    def clicked(self, button=1): # left = 1, right = 3
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == button:
                    return True
        return False

    def clicked_any(self):
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False

EventHandler = EventHandlerClass()

