from .settings import *

class GUIHandler:
    def __init__(self):
        self.fonts = {}
        self.title_font = pygame.font.Font(join("graphics", "fonts", "Goldman-Bold.ttf"), 75)

        self.screen = pygame.display.get_surface()

        # Respawn
        self.respawn_alpha = 0
        self.respawn_alpha_inc = 150
    
    def reset(self):
        self.respawn_alpha = 0

    def respawn_text(self, dt):
        self.respawn_alpha += self.respawn_alpha_inc * dt

        text = self.title_font.render("Press SPACE to Respawn", True, "White").convert_alpha()
        text.set_alpha(self.respawn_alpha)
        rect = text.get_frect(center = (self.screen.get_width() / 2, self.screen.get_height() / 2))

        top_text = self.title_font.render("You Died!", True, "White").convert_alpha()
        top_text.set_alpha(self.respawn_alpha)
        top_rect = top_text.get_frect(center = (rect.x + (rect.width / 2), rect.y - 40))

        self.screen.blit(text, rect)
        self.screen.blit(top_text, top_rect)