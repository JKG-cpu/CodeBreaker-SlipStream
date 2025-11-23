from settings import *
from entities import Player

class TransitionManager:
    def __init__(self, player: Player):
        self.player = player

        self.active = False
        self.mode = None
        self.surface = pygame.Surface((SCREEN_W, SCREEN_H))
        self.surface.fill((0, 0, 0))

        # Fade Transition
        self.alpha = 0
        self.fade_speed = 5
    
    def fade_in(self, speed: int = 300) -> None:
        self.mode = "fade_in"
        self.fade_speed = speed
        self.active = True
        self.alpha = 0

    def fade_out(self, speed: int = 300) -> None:
        self.mode = "fade_out"
        self.fade_speed = speed
        self.active = True
        self.alpha = 255
    
    def update(self, dt) -> None:
        if not self.active:
            return
        
        # Fade Transition
        if self.mode == "fade_in":
            self.alpha += self.fade_speed * dt
            if self.alpha >= 255:
                self.alpha = 255
                self.active = False
                self.player.block = True
    
        elif self.mode == "fade_out":
            self.alpha -= self.fade_speed * dt
            if self.alpha <= 0:
                self.alpha = 0
                self.active = False
                self.player.block = False
    
    def draw(self, screen: pygame.Surface):
        if self.active or self.alpha > 0:
            self.surface.set_alpha(self.alpha)
            screen.blit(self.surface, (0, 0))