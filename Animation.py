import pygame

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        return image

def create_sprite_animation(sheet_image_path, frame_width, frame_height, scale, steps):
    sprite_sheet_image = pygame.image.load(sheet_image_path).convert_alpha()
    sprite_sheet = SpriteSheet(sprite_sheet_image)
    frames = []

    for x in range(steps):
        frame = sprite_sheet.get_image(x, frame_width, frame_height, scale)
        frames.append(frame)

    return frames
