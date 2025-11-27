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

class ColliderRect(pygame.sprite.Sprite):
    def __init__(self, rect, groups):
        super().__init__(groups)
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

class ColliderPolygon(pygame.sprite.Sprite):
    def __init__(self, points, groups):
        super().__init__(groups)
        self.points = points

        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        width  = max_x - min_x
        height = max_y - min_y

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(min_x, min_y))

        # Debug
        pygame.draw.polygon(
            self.image,
            (255, 0, 0, 120),
            [(x - min_x, y - min_y) for x, y in points]
        )
