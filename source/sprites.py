from .settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, surf: pygame.Surface, pos: tuple[int, int], groups: pygame.sprite.Group):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class DeathZone(pygame.sprite.Sprite):
    def __init__(self, size: tuple[float, float], pos: tuple[float, float], groups):
        super().__init__(groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_frect(topleft = pos)