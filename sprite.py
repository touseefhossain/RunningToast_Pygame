import pygame
import spritesheet

# creation of a sprite class that will go through all images found in a spritesheet
# Credits to: Touseef Hossain (self-made)
class Sprite():

    # recieve spritesheet image and dimensions (assuming square) of one frame
    def __init__(self, sheet, dimension):
        self.spriteSheet = spritesheet.SpriteSheet(sheet)
        self.numFrames = sheet.get_width()//sheet.get_height()
        self.sprite_array = self.fillArray(dimension, dimension)
        self.index = 0

    # create and fill an array with all the different sprite images that form the animation
    def fillArray(self, width, height):
        self.sprite_array = []
        for x in range(self.numFrames):
            self.sprite_array.append(self.spriteSheet.getFrame(x, width, height))
        
        return self.sprite_array

    # iterate through the sprite array (go to next animation slide) by increasing the index
    def nextFrame(self):
        self.index += 1
        if self.index >= self.numFrames: self.index = 0
    
    # return the current frame that needs to be animated
    def currentFrame(self):
        return self.sprite_array[self.index]
