from .settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, color, health, death_zones, group):
        super().__init__(group)
        self.death_zones = death_zones

        self.direction = vector()

        self.max_health = health
        self.current_health = self.max_health

        self.speed = 250
        self.jump_power = -500
        self.gravity_amt = 700
        self.max_vel = 1500

        self.on_ground = False
        self.is_jumping = False
        self.jump_pressed = False
        self.double_jump = True
        self.freeze = False

        self.image = pygame.Surface((50, 50))
        self.orig_color = color
        self.image.fill(color)
        self.rect = self.image.get_frect(center = pos)

    def take_damage(self, amount: int) -> None:
        self.current_health -= amount

    def full_heal(self) -> None:
        self.current_health = self.max_health

    def heal(self, amount: int) -> None | bool:
        if self.current_health == self.max_health:
            return False
        self.current_health = min(self.max_health, self.current_health + amount)

    def gravity(self, dt):
        if self.freeze:
            return
        
        if not self.on_ground:
            self.direction.y += self.gravity_amt * dt

            if self.direction.y > self.max_vel:
                self.direction.y = self.max_vel

        elif type == "Horizontal":
            for sprite in self.collision_sprites:
                if self.rect.colliderect(sprite.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right

    def check_death(self):
        for sprite in self.death_zones:
            if self.rect.colliderect(sprite.rect):
                self.current_health = 0

    def reset(self):
        self.image.fill(self.orig_color)
        self.freeze = False
        self.direction = vector()
        self.full_heal()

    def death_effect(self):
        self.direction = vector()
        self.freeze = True
        self.image.fill("green")

    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.rect.centery += self.direction.y * dt

class Player(Entity):
    def __init__(self, pos, collision_sprites: pygame.sprite.Group, enemies: pygame.sprite.Group, death_zones: pygame.sprite.Group, group: pygame.sprite.Group):
        super().__init__(pos, "red", 100, death_zones, group)
        self.collision_sprites = collision_sprites
        self.enemies = enemies
        self.block = False
        self.sneak = False

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_c]:
            self.sneak = True
            self.direction.x = 0
            self.speed = 100

        else:
            self.sneak = False
            self.speed = 250

        if self.block:
            return

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

        self.on_ground = False

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

    def check_grounding(self):
        self.rect.bottom += 1
        
        collisions = pygame.sprite.spritecollideany(self, self.collision_sprites)
        
        self.rect.bottom -= 1
        
        if collisions:
            self.on_ground = True
            self.double_jump = True
        else:
            self.on_ground = False

    def respawn(self, point: tuple[int, int]):
        self.rect.center = point
        self.reset()

    def check_enemy_collisions(self):
        for sprite in self.enemies:
            if self.rect.colliderect(sprite.rect):
                self.current_health = 0

    def update(self, dt):
        self.check_grounding()

        self.input()
        self.gravity(dt)

        self.check_death()
        self.check_enemy_collisions()

        self.move(dt)

class Enemy(Entity):
    def __init__(self, pos, player: Player, collision_sprites: pygame.sprite.Group, group):
        super().__init__(pos, "White", 100, group)
        self.collision_sprites = collision_sprites

        self.player = player
        self.radius = 200
        self.speed = 200

    def handle_collisions(self, type):
        if type == "Vertical":
            for sprite in self.collision_sprites:
                if self.rect.colliderect(sprite.rect):
                    if self.direction.y > 0:
                        # Hitting the floor (setting position and zeroing velocity)
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                        self.on_ground = True # Essential for stopping gravity
                    
                    elif self.direction.y < 0:
                        # Hitting the ceiling
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0

        elif type == "Horizontal":
            for sprite in self.collision_sprites:
                if self.rect.colliderect(sprite.rect):
                    if self.direction.x > 0:
                        # Hitting a wall on the right
                        self.rect.right = sprite.rect.left
                        self.direction.x = 0 # <-- Stops sticking
                        
                    elif self.direction.x < 0:
                        # Hitting a wall on the left
                        self.rect.left = sprite.rect.right
                        self.direction.x = 0 # <-- Stops sticking

    def check_grounding(self):
        self.rect.bottom += 1
        
        is_grounded = pygame.sprite.spritecollideany(self, self.collision_sprites)
        
        self.rect.bottom -= 1
        
        if is_grounded:
            self.on_ground = True
        else:
            self.on_ground = False

    def in_range(self, player_center: tuple[int, int]) -> bool:
        if self.player.sneak:
            return
        
        player_x, player_y = player_center
        
        dx = self.rect.centerx - player_x
        dy = self.rect.centery - player_y
        
        distance_sq = (dx * dx) + (dy * dy)
        
        if distance_sq <= (self.radius * self.radius):
            return True
        return False

    def follow(self, player_center: tuple[int, int]):
        in_range = self.in_range(player_center) 
        
        if in_range:
            player_x = player_center[0]
            if player_x > self.rect.centerx:
                self.direction.x = 1
            
            elif player_x < self.rect.centerx:
                self.direction.x = -1
            
        else:
            self.direction.x = 0
    
    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.handle_collisions("Horizontal")

        self.rect.centery += self.direction.y * dt
        self.handle_collisions("Vertical")

    def update(self, dt):
        # Check on or off ground
        self.check_grounding()

        # Apply Gravity
        self.gravity(dt)

        # Move Enemy        
        self.follow(self.player.rect.center)
        self.move(dt)
