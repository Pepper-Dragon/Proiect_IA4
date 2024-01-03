import pygame.sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, image: pygame.Surface, position: tuple, parameters: dict):
        super().__init__(groups)
        self.image = image
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=position)

        self.velocity = pygame.math.Vector2(0, 0)

    def input(self):
        self.velocity.x = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.velocity.x = -5

        if keys[pygame.K_d]:
            self.velocity.x = 5

    def move(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def update(self):
        self.input()
        self.move()