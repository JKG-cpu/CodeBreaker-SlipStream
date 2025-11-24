from settings import *
from entities import Player

class TransitionManager:
    def __init__(self, player: Player):
        self.player = player

        self.transitions = {
            "fade_in": lambda speed: self.fade_in(speed),
            "fade_out": lambda speed: self.fade_out(speed)
        }

        self.active = False
        self.mode = None
        self.surface = pygame.Surface((SCREEN_W, SCREEN_H))
        self.surface.fill((0, 0, 0))

        # Fade Transition
        self.alpha = 0
        self.fade_speed = 5
        self.faded_in = False
    
    # Run a Transition
    def run_transition(self, type: str, args = None) -> None:
        """
        Transition Types

        - fade_in
        - fade_out
        """
        self.transitions[type](args)

    # Transitions
    def fade_in(self, speed: int = None) -> None:
        self.mode = "fade_in"

        if speed is None:
            self.fade_speed = 300
        else:
            self.fade_speed = speed

        self.active = True
        self.faded_in = True
        self.alpha = 0

    def fade_out(self, speed: int = None) -> None:
        self.mode = "fade_out"

        if speed is None:
            self.fade_speed = 300
        else:
            self.fade_speed = speed

        self.active = True
        self.alpha = 255
    
    # Update & Draw Transitions
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
                self.faded_in = False
                self.player.block = False
    
    def draw(self, screen: pygame.Surface):
        if self.active or self.alpha > 0:
            self.surface.set_alpha(self.alpha)
            screen.blit(self.surface, (0, 0))