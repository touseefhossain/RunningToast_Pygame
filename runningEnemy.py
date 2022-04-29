import pygame
import sprite
from random import randint

class Enemy():

    pygame.image.load('Graphics/toaster_move.png')
    pygame.image.load('Graphics/egg_move.png')
    
    def __init__(self, type):
        if type == 'egg':
            egg_move_image = pygame.image.load('Graphics/egg_move.png')
            self.sprite_move = sprite.Sprite(egg_move_image, 64)
            self.speed = 5
            self.height = 280
        else:
            toaster_move_image = pygame.image.load('Graphics/toaster_move.png')
            self.sprite_move = sprite.Sprite(toaster_move_image, 64)
            self.speed = 4
            self.height = 380
        self.image = self.sprite_move.currentFrame()
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), self.height))
    
    def move(self, screen):
        self.rect.left -= self.speed
        screen.blit(self.image, self.rect)

    def outOfBounds(self):
        if self.rect.left <= -100: return True
        else: return False

    def animate(self):
        self.sprite_move.nextFrame()
        self.image = self.sprite_move.currentFrame()

    def getRect(self):
        return self.rect