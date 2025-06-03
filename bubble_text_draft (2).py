import pygame
import Animation 

pygame.init()

width = 1280 #DONE
height = 720 #DONE

screen = pygame.display.set_mode((width, height)) #done
pygame.display.set_caption('sprites') #done

sprite_sheet_image = pygame.image.load('hangabubu_textsprites.png').convert_alpha()
sprite_sheet = Animation.SpriteSheet(sprite_sheet_image)

BG = (255,209,220)

#create animation list
animation_list = []
animation_steps = [2,2,2,2,2,2,2,2,2]
action = 4
last_update = pygame.time.get_ticks()
animation_cooldown = 500
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 200, 200, 3))
        step_counter += 1
    animation_list.append(temp_img_list)

print(animation_list)

run = True
while run:

    screen.fill(BG)

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    screen.blit(animation_list[action][frame], (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()
    
pygame.quit()


