import pygame
from Animation import create_sprite_animation  # if you saved the function separately

pygame.init()

# Screen setup
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sprite Animation Function')

# Background color
BG = (50, 50, 50)
BLACK = (0, 0, 0)

# Animation setup
animation_frames = create_sprite_animation(
    'hangabubu_scared.png', 200, 200, 1.0, 2, BLACK
)

# Animation control variables
frame_index = 0
animation_cooldown = 20  # milliseconds
last_update = pygame.time.get_ticks()

# Game loop
run = True
while run:
    screen.fill(BG)

    # Timing & frame switching
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame_index = (frame_index + 1) % len(animation_frames)
        last_update = current_time

    # Draw frame
    screen.blit(animation_frames[frame_index], (100, 100))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
