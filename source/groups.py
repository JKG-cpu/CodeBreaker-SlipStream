from .settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

        self.offset = vector()
        self.target_offset = vector()

        # Deadzone in the center of the screen
        self.deadzone = pygame.Rect(
            SCREEN_W//2 - 80,
            SCREEN_H//2 - 50,
            200,
            150
        )

        self.smoothness = 0.05

    def update_camera(self, player_rect):
        player_screen_x = player_rect.centerx + self.offset.x
        player_screen_y = player_rect.centery + self.offset.y

        # --- Deadzone logic ---
        if player_screen_x < self.deadzone.left:
            self.deadzone.left = player_screen_x
        if player_screen_x > self.deadzone.right:
            self.deadzone.right = player_screen_x
        if player_screen_y < self.deadzone.top:
            self.deadzone.top = player_screen_y
        if player_screen_y > self.deadzone.bottom:
            self.deadzone.bottom = player_screen_y

        # Camera target = move camera so deadzone comes back to center.
        deadzone_center = vector(self.deadzone.centerx, self.deadzone.centery)

        self.target_offset.x = -(deadzone_center.x - SCREEN_W / 2)
        self.target_offset.y = -(deadzone_center.y - SCREEN_H / 2)

        # Smooth LERP
        self.offset += (self.target_offset - self.offset) * self.smoothness

    def draw(self, player_rect):
        self.update_camera(player_rect)

        for sprite in self:
            pos = sprite.rect.topleft + self.offset
            self.screen.blit(sprite.image, pos)

class DeathZones(pygame.sprite.Group):
    pass