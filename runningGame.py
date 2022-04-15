import pygame
from sys import exit
import spritesheet

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 400
running = True

# display screen settings
pygame.init() # initialize the pygame module (like starting a car with key)
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT)) # display size
pygame.display.set_caption('RunningToast')
timer = pygame.time.Clock()
bgTextStyle = pygame.font.Font('Grand9K Pixel.ttf', 50)

background =  pygame.image.load('Graphics/kitchen_BG.jpg').convert()
background = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
bgX = 0
bgX2 = DISPLAY_WIDTH
bgText = bgTextStyle.render('Run, ma boi', False, 'white')
bgText_rect = bgText.get_rect(center=(400, 50))

# Code sampled and derived from
# https://www.techwithtim.net/tutorials/game-development-with-python/side-scroller-pygame/background/
def redrawBackground():
    global bgX, bgX2
    screen.blit(background, (bgX,0))
    screen.blit(background, (bgX2, 0))
    # draws background colour and shape for a specified rectangle
    pygame.draw.rect(screen, 'slateblue3', bgText_rect, border_radius = 20)
    screen.blit(bgText, bgText_rect)
    # move both images in same direction to simulate scrolling background
    bgX -= 1.1
    bgX2 -= 1.1
    # reset the image positions once they reach the end
    if bgX < -DISPLAY_WIDTH:
        bgX = DISPLAY_WIDTH
    if bgX2 < -DISPLAY_WIDTH:
        bgX2 = DISPLAY_WIDTH

toast_move_image = pygame.image.load('Graphics/toast_move.png').convert_alpha()
toast_move_spread = spritesheet.SpriteSheet(toast_move_image)

toast_move_01 = toast_move_spread.getFrame(0, 64, 64)
toast_rect = toast_move_01.get_rect(midbottom =(60, 380))
toast_gravity = 0
pygame.display.set_icon(toast_move_01) # set window icon

# load obstacle objects
egg_move_image = pygame.image.load('Graphics/egg_move.png').convert_alpha()
egg_move_spread = spritesheet.SpriteSheet(egg_move_image)
egg_move_01 = egg_move_spread.getFrame(0, 64, 64)
egg_rect = egg_move_01.get_rect(center = (900, 260))


while running: # ensure that program doesn't end unless prompted
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # close the window 'X'
            pygame.quit() # cancel the pygame module
            running = False
            exit() # leave the 'while TRUE' loop securely with sys exit
        if event.type == pygame.KEYDOWN: # keyboard inputs
            if event.key == pygame.K_SPACE: # spacebar key
                if toast_rect.bottom == 380: # ensure only a single jump from ground
                    toast_gravity = -20 # when pressed, send toast upwards
    
    redrawBackground()
    screen.blit(toast_move_01, toast_rect)
    screen.blit(egg_move_01, egg_rect)

    # simulate jumping with gravity
    toast_gravity+=1
    toast_rect.y += toast_gravity

    # movement of egg obstacle
    egg_rect.left -= 3
    if egg_rect.left < -100: egg_rect.left = 801

    # maintain floor for toast player
    if toast_rect.bottom >= 380: 
        toast_rect.bottom = 380
        toast_gravity = 0 # reset gravity, rather than have gravity infinitely increasing

    pygame.display.update() # updates the display continuously
    timer.tick(60) # ensure that while loop does not run more than 60 times per second (max frame rate)
