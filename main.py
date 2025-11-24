from source import *

class Main:
    def __init__(self):
        # Init
        pygame.init()

        # Setup Basic Screen
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("CodeBreaker: SlipStream")

        # Framerate
        self.clock = pygame.time.Clock()

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Player
        self.player_respawn_point = (50, 50)
        self.player = Player((50, 50), self.collision_sprites, self.enemies, self.all_sprites)
        self.cam_target_rect = None
        self.wait_for_respawn = False

        # Test Enemy
        self.enemy = Enemy((300, 100), self.player, self.collision_sprites, (self.all_sprites, self.enemies))

        # Effects
        self.transitions = TransitionManager(self.player)
        self.flashlight = FlashLight(self.player)

        # Gui
        self.gui = GUIHandler()

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
                
                if event.key == pygame.K_SPACE and self.transitions.alpha == 255:
                    self.transitions.fade_out()
                    self.player.respawn(self.player_respawn_point)
                    self.gui.reset()
                    self.wait_for_respawn = False

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
            if self.wait_for_respawn:
                self.all_sprites.draw(self.cam_target_rect)

            else:
                self.all_sprites.draw(self.player.rect)

            self.all_sprites.update(dt)

            # Handle Transitions
            if self.player.current_health == 0 and not self.transitions.faded_in:
                self.player.death_effect()
                self.transitions.run_transition(type = "fade_in")
                self.cam_target_rect = self.player.rect.copy()
                self.wait_for_respawn = True

            self.transitions.update(dt)
            self.transitions.draw(self.screen)

            if self.player.sneak:
                self.flashlight.flashlight(self.all_sprites.offset)

            # Main GUI
            if self.wait_for_respawn:
                self.gui.respawn_text(dt)

            # Update Display
            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.play()