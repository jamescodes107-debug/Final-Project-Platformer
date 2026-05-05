import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        original_image = pygame.image.load("player.png").convert_alpha()
        self.image_right = pygame.transform.scale(original_image, (width, height))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        
        self.image = self.image_right
        self.facing_right = True
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Physics properties
        self.vel_y = 0
        self.vel_x = 0
        self.speed = 5
        self.gravity = 0.5
        self.jump_strength = -10
        self.on_ground = False
        
        # Dash properties
        self.can_dash = True
        self.is_dashing = False
        self.dash_speed = 30
        self.dash_max_duration = 5
        self.dash_timer = 0

    def update(self, platforms):
        self.handle_input()
        
        if self.is_dashing:
            self.dash_timer -= 1
            self.vel_x = self.dash_speed if self.facing_right else -self.dash_speed
            self.vel_y = 0
            if self.dash_timer <= 0:
                self.is_dashing = False
        else:
            # Apply vertical movement (gravity)
            self.vel_y += self.gravity

        # Apply horizontal movement
        self.rect.x += self.vel_x
        self.check_horizontal_collisions(platforms)
        
        # Apply vertical movement
        self.rect.y += self.vel_y
        self.check_vertical_collisions(platforms)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_d]:
            self.vel_x = self.speed
            if not self.facing_right:
                self.image = self.image_right
                self.facing_right = True
        if keys[pygame.K_a]:
            self.vel_x = -self.speed
            if self.facing_right:
                self.image = self.image_left
                self.facing_right = False

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump()
            
        if keys[pygame.K_LSHIFT] and self.can_dash and not self.on_ground and not self.is_dashing:
            self.is_dashing = True
            self.can_dash = False
            self.dash_timer = self.dash_max_duration

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    def check_horizontal_collisions(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.vel_x > 0: # Moving right, hit left side of platform
                self.rect.right = hit.rect.left
            elif self.vel_x < 0: # Moving left, hit right side of platform
                self.rect.left = hit.rect.right

    def check_vertical_collisions(self, platforms):
        self.on_ground = False
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.vel_y > 0: # Falling, hit top of platform
                self.rect.bottom = hit.rect.top
                self.vel_y = 0
                self.on_ground = True
                self.can_dash = True
            elif self.vel_y < 0: # Jumping up, hit bottom of platform
                self.rect.top = hit.rect.bottom
                self.vel_y = 0