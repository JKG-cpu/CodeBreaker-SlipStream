from .settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, surf: pygame.Surface, pos: tuple[int, int], groups: pygame.sprite.Group):
        super().__init__(groups)
        self.image = surf
        self.image.fill("blue")
        self.rect = self.image.get_frect(topleft = pos)