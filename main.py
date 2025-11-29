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

        # Gui
        self.gui = GUIHandler()

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.death_zones = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.import_assests()
        self.setup(self.tile_maps["Tutorial"])

        # Player
        self.cam_target_rect = self.player.rect.copy()
        self.wait_for_respawn = False

        # Effects
        self.transitions = TransitionManager(self.player)
        self.flashlight = FlashLight(self.player)

    def import_assests(self):
        self.tile_maps = {
            "Tutorial": load_pygame(join("graphics", "maps", "tmx", "map1.tmx"))
        }

        self.frames = {
            "Player": import_character("graphics", "images", "Player")
        }

        self.background1 = scale_image(2, "graphics", "images", "Enviro", "BG01.png")
        self.background2 = scale_image(2, "graphics", "images", "Enviro", "BG02.png")

    def setup(self, tmx_map: TiledMap):
        # --- Main Tiles ---
        floor_layer = tmx_map.get_layer_by_name("Floor 1")
        for x, y, gid in floor_layer.iter_data():
            if not gid:
                continue

            surf = tmx_map.get_tile_image_by_gid(gid)
            tile_propetries = tmx_map.get_tile_properties_by_gid(gid)

            if tile_propetries.get("Hitbox"):
                for obj in tile_propetries.get("colliders", []):
                    world_x = x * TILE_SIZE
                    world_y = y * TILE_SIZE

                    if obj.width and obj.height:
                        rect = pygame.Rect(
                            world_x + obj.x,
                            world_y + obj.y,
                            obj.width,
                            obj.height
                        )
                        Sprite(surf, (rect.x, rect.y), self.all_sprites)
                        ColliderRect(rect, self.collision_sprites)

                    elif hasattr(obj, "points"):
                        world_points = [
                            (world_x + px, world_y + py)
                            for px, py in obj.points
                        ]
                        Sprite(surf, (obj.x, obj.y), self.all_sprites)
                        ColliderPolygon(world_points, self.collision_sprites)
                    
                    else:
                        print("Unknown collider type: ", obj)
            
            else:
                Sprite(
                    surf = surf,
                    pos = (x * TILE_SIZE, y * TILE_SIZE),
                    groups = (self.all_sprites, self.collision_sprites)
                )

        # --- Death Zones ---
        for obj in tmx_map.get_layer_by_name("Death Zones"):
            DeathZone((obj.width, obj.height), (obj.x, obj.y), self.death_zones)

        # --- Player ---
        for obj in tmx_map.get_layer_by_name("Spawns"):
            if obj.name == "Player":
                self.player_respawn_point = (obj.x, obj.y)
                self.player = Player(
                    frames = self.frames["Player"],
                    pos = (obj.x, obj.y),
                    collision_sprites = self.collision_sprites,
                    enemies = self.enemies,
                    death_zones = self.death_zones,
                    group = self.all_sprites
                )

        # --- Text ---
        for obj in tmx_map.get_layer_by_name("GUI"):
            self.gui.new_text((obj.x, obj.y), obj.Text)

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
            # Fill Screen / Load in Background
            self.screen.fill("Black")
            self.screen.blit(self.background2, (0, 0))
            self.screen.blit(self.background1, (0, 0))

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

            # Text Display
            self.gui.display_texts(self.all_sprites.offset)

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