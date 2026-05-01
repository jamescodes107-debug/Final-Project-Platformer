import pygame
pygame.init()

width = 800
height = 600
gravity = 1
vel_y = 0

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
player_rect = pygame.Rect(400, 100, 50, 50)

game_over = False


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_rect.y -= 10
    vel_y += gravity
    player_rect.y += vel_y 




pygame.quit()
