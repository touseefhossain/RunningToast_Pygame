import pygame
import sprite

class Toast():

    def __init__(self):
        move_animation = pygame.image.load('Graphics/toast_move.png')
        self.sprite_move = sprite.Sprite(move_animation, 64)
        self.image = self.sprite_move.currentFrame()
        self.rect = self.image.get_rect(midbottom = (60, 380))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('Audio/SonicJump.mp3')
        self.jump_sound.set_volume(0.7)
        self.jump_anim = pygame.image.load('Graphics/toast_jump.png')
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 380: 
            self.gravity = -16
            self.jump_sound.play()
        
    
    def apply_gravity(self):
        self.gravity += 0.6
        self.rect.y += self.gravity
        if self.rect.bottom >= 380:
            self.rect.bottom = 380
            self.gravity = 0
            self.image = self.sprite_move.currentFrame()
        else: self.image = self.jump_anim

    def animate(self):
        self.sprite_move.nextFrame()

    def getRect(self):
        return self.rect

    def reset(self):
        self.rect.bottom = 380
        self.gravity = 0

    def update(self, screen):
        self.player_input()
        self.apply_gravity()
        screen.blit(self.image, self.rect)