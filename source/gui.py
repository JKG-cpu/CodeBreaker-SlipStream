from .settings import *

class GUIHandler:
    def __init__(self):
        self.fonts = {}
        self.title_font = pygame.font.Font(join("graphics", "fonts", "Goldman-Bold.ttf"), 75)
        self.font = pygame.font.Font(join("graphics", "fonts", "Goldman-Bold.ttf"), 25)

        self.screen = pygame.display.get_surface()

        # Respawn
        self.respawn_alpha = 0
        self.respawn_alpha_inc = 150

        # Texts
        self.texts = []

    # Reset Everything
    def reset(self):
        self.respawn_alpha = 0

    # Respawn
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

    # Help Text
    def new_text(self, pos: tuple[int, int], text: str):
        help_text = self.font.render(text, True, "White")
        help_text_rect = help_text.get_frect(center = pos)

        self.texts.append((help_text, help_text_rect))
    
    def display_texts(self, offset: vector):
        for text, rect in self.texts:
            self.screen.blit(text, rect.topleft + offset)