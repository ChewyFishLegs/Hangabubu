import pygame


	
pygame.init()

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image
	
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('hangabubu_nervous_spritesheet.png').convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)


BG = (50, 50, 50) 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#creae animation lit
animation_list = []
animation_steps = 8
last_update = pygame.time.get_ticks()
animation_cooldown = 200
frame = 0

for x in range(animation_steps):
	animation_list.append(SpriteSheet.get_image(sprite_sheet, x, 98, 98, 1.0, BLACK))

run = True
while run:

	#update background
	screen.fill(BG)

	#show frame image
	current_time = pygame.time.get_ticks()
	if current_time - last_update >= animation_cooldown:
		frame = (frame + 1) % animation_steps
		last_update = current_time

	screen.blit(animation_list[frame], (0,0))
	

	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()