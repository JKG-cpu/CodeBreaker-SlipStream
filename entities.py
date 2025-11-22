from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, color, group):
        super().__init__(group)

        self.direction = vector()
        self.speed = 250

        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_frect(center = pos)

        self.on_ground = False

    def gravity(self, dt):
        if not self.on_ground:
            self.direction.y += GRAVITY * dt

            if self.direction.y > MAX_FALLING_SPEED:
                self.direction.y = MAX_FALLING_SPEED

class Player(Entity):
    def __init__(self, pos, collision_sprites: pygame.sprite.Group, group):
        super().__init__(pos, "red", group)
        self.collision_sprites = collision_sprites

    def input(self):
        direction = vector()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            direction.x = -1
        
        if keys[pygame.K_RIGHT]:
            direction.x = 1

        self.direction.x = direction.x

    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt

        self.rect.centery += self.direction.y * self.speed * dt
        self.handle_collisions("Vertical")

    def handle_collisions(self, type):
        if type == "Horizontal":
            pass

        else:
            self.on_ground = False
            
            for sprite in self.collision_sprites:
                if self.rect.colliderect(sprite.rect):
                    if self.direction.y > 0: # Player is falling
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.on_ground = True
                    
                    elif self.direction.y < 0: # Player is hitting their head on something
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0

    def update(self, dt):
        self.input()
        self.gravity(dt)
        self.move(dt)