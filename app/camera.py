import pygame.sprite

from player import Player


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.bg = pygame.image.load('assets/Background/2.png').convert_alpha()

        #     scale background
        self.bg = pygame.transform.scale(self.bg, (self.bg.get_width() * 2, self.bg.get_height() * 2))

    def draw(self, target: Player, display: pygame.Surface, balls, dynamic_objects):
        display.blit(self.bg, (0, 0))

        offset = pygame.math.Vector2()
        offset.x = display.get_width() / 2 - target.ball.collider.centerx
        offset.y = display.get_height() / 2 - target.ball.collider.centery + 150

        for sprite in self.sprites():
            sprite_offset = offset + sprite.rect.topleft

            display.blit(sprite.image, sprite_offset)

        for ball in balls:
            ball.draw(display, offset)

        for obj in dynamic_objects:
            obj.draw(display, offset)

#         draw player
        target.draw(offset)


