#spritesheet class that retrieves a frame in a sprite sheet
import pygame

# code from https://www.youtube.com/watch?v=M6e3_8LHc7A&ab_channel=CodingWithRuss
class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    
    def getFrame(self, frame, width, height):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image.set_colorkey('black') # makes background of image transparent
        return image