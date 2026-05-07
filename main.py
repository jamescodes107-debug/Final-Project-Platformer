import pygame
from Player import Player
from Platform import Platform
from Hazard import Hazard
from Goal import Goal

pygame.init()

# Screen dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Final Project Platformer")

clock = pygame.time.Clock()
FPS = 60

# Fonts for messages
font = pygame.font.SysFont(None, 48)

# Level design
# Each block is 40x40. Grid is 20x15.
# P = Platform, L = Lava (Hazard), G = Goal, S = Start Position (Player)
level_grid = [
        "                    ",
        "G                   ",
        "PP                 L",
        "     LLP     P     D",
        "     PPP           D",
        "       P           D",
        "       D  L   LL   D",
        "       D  P   PD    ",
        "          P   PD    ",
        "          P   PD    ",
        "          D         ",
        "S  PPP    D         ",
        "P         D   LL  P ",
        "          P   PP    ",
        "PPLLLLLLLLPLLLPPLLLL"
    ]

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
hazards = pygame.sprite.Group()
goals = pygame.sprite.Group()

start_x = 0
start_y = 0
block_size = 40

# Build level from grid
for row_idx, row in enumerate(level_grid):
    for col_idx, char in enumerate(row):
        x = col_idx * block_size
        y = row_idx * block_size
        
        if char == "P":
            p = Platform(x, y, block_size, block_size)
            platforms.add(p)
            all_sprites.add(p)
        elif char == "D":
            p = Platform(x, y, block_size, block_size, double_jump_platform=True)
            platforms.add(p)
            all_sprites.add(p)
        elif char == "L":
            h = Hazard(x, y + 20, block_size, 20) # Half height for lava
            hazards.add(h)
            all_sprites.add(h)
        elif char == "G":
            g = Goal(x, y, block_size, block_size)
            goals.add(g)
            all_sprites.add(g)
        elif char == "S":
            start_x = x
            start_y = y

# Create player
player = Player(start_x, start_y, 40, 40)
all_sprites.add(player)

game_over = False
win = False

# Main Game Loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            
        if not win:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()

    if not win:
        player.update(platforms)
        
        # Check hazards (Lava)
        if pygame.sprite.spritecollide(player, hazards, False):
            # Respawn player
            player.rect.x = start_x
            player.rect.y = start_y
            player.vel_y = 0
            player.vel_x = 0

        # Check goal
        if pygame.sprite.spritecollide(player, goals, False):
            win = True

        # Fall off map
        if player.rect.y > height:
            player.rect.x = start_x
            player.rect.y = start_y
            player.vel_y = 0
            player.vel_x = 0
            
        if player.rect.right > width:
            player.rect.right = width
        if player.rect.left < 0:
            player.rect.left = 0

    screen.fill((135, 206, 235))
    
    all_sprites.draw(screen)
    
    if win:
        text = font.render("You Win!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width/2, height/2))
        screen.blit(text, text_rect)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
