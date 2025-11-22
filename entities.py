from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, color, group):
        super().__init__(group)

        self.direction = vector()

        self.speed = 250
        self.jump_power = -500
        self.gravity_amt = 700
        self.max_vel = 1500

        self.on_ground = False
        self.is_jumping = False
        self.jump_pressed = False
        self.double_jump = True

        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_frect(center = pos)

    def gravity(self, dt):
        if not self.on_ground:
            self.direction.y += self.gravity_amt * dt

            if self.direction.y > self.max_vel:
                self.direction.y = self.max_vel

class Player(Entity):
    def __init__(self, pos, collision_sprites: pygame.sprite.Group, group):
        super().__init__(pos, "red", group)
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1

        if keys[pygame.K_UP]:
            if not self.jump_pressed:
                if self.on_ground:
                    self.jump()
                    self.jump_pressed = True

                elif self.double_jump:
                    self.jump()
                    self.double_jump = False
                    self.jump_pressed = True
            
        else:
            self.jump_pressed = False

    def jump(self):
        self.direction.y = self.jump_power
        self.is_jumping = True
        self.on_ground = False

    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.handle_collisions("Horizontal")

        self.rect.centery += self.direction.y * dt
        self.handle_collisions("Vertical")

    def handle_collisions(self, type):
        if type == "Vertical":
            for sprite in self.collision_sprites:
                if self.rect.colliderect(sprite.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.on_ground = True
                        self.is_jumping = False
                        self.double_jump = True

                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0

        elif type == "Horizontal":
            for sprite in self.collision_sprites:
                if self.rect.colliderect(sprite.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right

    def update(self, dt):
        self.input()
        self.gravity(dt)
        self.move(dt)
