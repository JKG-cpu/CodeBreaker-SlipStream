from settings import *
from entities import Entity, Player, Enemy
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
        self.enemy = Enemy((100, 150), self.player, self.collision_sprites, self.all_sprites)

        self.ground_surface = pygame.Surface((SCREEN_W, 50))
        self.ground = Sprite(self.ground_surface, (0, SCREEN_H - 50), (self.all_sprites, self.collision_sprites))

        self.top_surface = pygame.Surface((100, 50))
        self.top = Sprite(self.top_surface, (50, SCREEN_H - 250), (self.all_sprites, self.collision_sprites))

    def handle_events(self, events):
        for event in events:
            # Quitting
            if event.type == pygame.QUIT:
                self.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    def quit(self):
        pygame.quit()
        cc()
        close_game()

    def play(self) -> None:
        while True:
            # Fill Screen
            self.screen.fill("Black")

            # DT
            dt = self.clock.tick() / 1000

            # Event Loop
            events = pygame.event.get()
            self.handle_events(events)

            # Main Logic
            self.all_sprites.draw()
            self.all_sprites.update(dt)

            # Update Display
            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.play()