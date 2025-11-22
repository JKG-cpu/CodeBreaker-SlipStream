from settings import *
from entities import Entity, Player
from groups import AllSprites
from sprites import Sprite

class Main:
    def __init__(self):
        # Setup Basic Screen
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("CodeBreaker: SlipStream")

        self.clock = pygame.time.Clock()

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # Player
        self.player = Player((50, 50), self.collision_sprites, self.all_sprites)

        self.ground_surface = pygame.Surface((100, 50))
        self.ground = Sprite(self.ground_surface, (50, 150), (self.all_sprites, self.collision_sprites))

    def play(self) -> None:
        while True:
            # Fill Screen
            self.screen.fill("Black")

            # DT
            dt = self.clock.tick() / 1000

            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    cc()
                    close_game()

            # Main Logic
            self.all_sprites.draw()
            self.all_sprites.update(dt)

            # Update Display
            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.play()