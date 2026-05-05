import pygame

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 215, 0)) # Gold for goal
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
