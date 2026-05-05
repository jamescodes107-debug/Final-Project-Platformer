import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(0, 255, 0), double_jump_platform=False):
        super().__init__()
        self.image = pygame.Surface((width, height))
        if double_jump_platform:
            self.image.fill((0, 0, 255)) # Blue for double jump
        else:
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.double_jump_platform = double_jump_platform
