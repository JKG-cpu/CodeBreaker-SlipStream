from .settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

        self.offset = vector()
        self.target_offset = vector()
        self.deadzone = pygame.Rect(0, 0, 200, 150)
        
        self.smoothness = 0.05

    def update_camera(self, player_rect):
        # --- Deadzone Logic (World Space) ---
        # Instead of moving the camera immediately, move the deadzone box if the player pushes against its edges.

        if player_rect.right > self.deadzone.right:
            self.deadzone.right = player_rect.right
        
        if player_rect.left < self.deadzone.left:
            self.deadzone.left = player_rect.left
            
        if player_rect.bottom > self.deadzone.bottom:
            self.deadzone.bottom = player_rect.bottom
            
        if player_rect.top < self.deadzone.top:
            self.deadzone.top = player_rect.top

        # --- Camera Scroll ---
        self.target_offset.x = (SCREEN_W / 2) - self.deadzone.centerx
        self.target_offset.y = (SCREEN_H / 2) - self.deadzone.centery

        # Smooth LERP
        self.offset += (self.target_offset - self.offset) * self.smoothness

    def draw(self, player_rect):
        self.update_camera(player_rect)

        for sprite in self:
            pos = sprite.rect.topleft + self.offset
            self.screen.blit(sprite.image, pos)

        pygame.draw.rect(self.screen, "Blue", self.deadzone)