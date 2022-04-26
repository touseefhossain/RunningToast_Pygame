# simple running game developed by Touseef Hossain
# tutorial content used in this code found from
# https://www.youtube.com/watch?v=AY9MnQ4x3zk
import pygame
from sys import exit
from random import randint
import spritesheet
import sprite

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 400
running = True

# window and frame settings
pygame.init() # initialize the pygame module (like starting a car with key)
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT)) # display size
pygame.display.set_caption('RunningToast')
timer = pygame.time.Clock()
bgTextStyle = pygame.font.Font('Grand9K Pixel.ttf', 50)

# 'playing' state background settings
background =  pygame.image.load('Graphics/kitchen_BG.jpg').convert()
background = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
bgX = 0
bgX2 = DISPLAY_WIDTH
bgSpeed = 2

timeTextStyle = pygame.font.Font('Grand9K Pixel.ttf', 20)
start_time = 0 # timer that will help with maintaining accurate time whenever the game restarts
game_time = 0 # used to display total play time for a game

score = 0

# 'game over' state background settings
gg_text = bgTextStyle.render('Game Over', False, 'white')
gg_rect = gg_text.get_rect(center =(400, 80))
gg_continue_text = timeTextStyle.render('Try Again? ( SPACE )', False, 'white')
gg_continue_rect = gg_continue_text.get_rect(center = (400, 350))

toast_defeat_image = pygame.image.load('Graphics/toast_defeat.png').convert_alpha()
toast_defeat_sprite = spritesheet.SpriteSheet(toast_defeat_image)
toast_defeat_surface = toast_defeat_sprite.getFrame(0, 64, 64)
toast_defeat_surface = pygame.transform.rotozoom(toast_defeat_surface, 0, 1.6) # filter, scale, rotate
toast_defeat_surface.set_colorkey('black')
toast_defeat_rect = toast_defeat_surface.get_rect(center = (400, 200))

def displayTime():
    global game_time
    current_time = pygame.time.get_ticks() - start_time
    game_time = formatTime(current_time)
    time_surface = timeTextStyle.render(f'{game_time}', False, 'white') # f string method to print int
    time_rect = time_surface.get_rect(center=(100, 50))
    pygame.draw.rect(screen, 'slateblue3', time_rect)
    screen.blit(time_surface, time_rect)

def formatTime(time):
    seconds = time//1000 # minimum integer division
    minutes = 0
    while seconds >= 60: # get number of minutes
        minutes += 1
        seconds -= 60
    
    # ensure there's always two digits shown on each time interval
    seconds = str(seconds).zfill(2)
    minutes = str(minutes).zfill(2)
    return f'{minutes}:{seconds}'

def displayScore():
    adjusted_score = str(score).zfill(2)
    score_surface = timeTextStyle.render(f'{adjusted_score}', False, 'slateblue3')
    score_rect = score_surface.get_rect(center = (700, 50))
    screen.blit(score_surface, score_rect)

# Code sampled and derived from
# https://www.techwithtim.net/tutorials/game-development-with-python/side-scroller-pygame/background/
def redrawBackground():
    global bgX, bgX2
    screen.blit(background, (bgX,0))
    screen.blit(background, (bgX2, 0))

    displayTime()
    displayScore()

    # move both images in same direction to simulate scrolling background
    bgX -= bgSpeed
    bgX2 -= bgSpeed

    # reset the image positions once they reach the end
    if bgX < -DISPLAY_WIDTH:
        bgX = DISPLAY_WIDTH
    if bgX2 < -DISPLAY_WIDTH:
        bgX2 = DISPLAY_WIDTH

# initiate timer for sprite animation
sprite_frame_rate = 100
sprite_timer = pygame.USEREVENT + 1
pygame.time.set_timer(sprite_timer, sprite_frame_rate)

# load player object and initiate player parameters
toast_move_image = pygame.image.load('Graphics/toast_move.png').convert_alpha()
toast_move_sprite = sprite.Sprite(toast_move_image, 64)
toast_rect = toast_move_sprite.currentFrame().get_rect(midbottom =(60, 380))
toast_gravity = 0
pygame.display.set_icon(toast_move_sprite.currentFrame()) # set window icon

# load obstacle objects
egg_move_image = pygame.image.load('Graphics/egg_move.png').convert_alpha()
egg_move_sprite = sprite.Sprite(egg_move_image, 64)

toaster_move_image = pygame.image.load('Graphics/toaster_move.png').convert_alpha()
toaster_move_sprite = sprite.Sprite(toaster_move_image, 64)

# initiate timer for enemy spawn rate and list for enemies present on screen
enemy_spawn_rate = 3000
enemy_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_timer, enemy_spawn_rate)
enemy_list = []

# move the obstacles according to their respective type
def enemyMovement(list):
    global score
    if list:
        for enemy in list:
            if enemy.centery == 250:
                enemy.left -= 5
                screen.blit(egg_move_sprite.currentFrame(), enemy)
            else:
                enemy.left -= 4
                screen.blit(toaster_move_sprite.currentFrame(), enemy)
            if enemy.left <= -100:
                list.remove(enemy)
                score += 1
        return list
    else: return []

game_active = True # state of the game (switch from playing and 'game over' screen)

# check for collisions between player and obstacles
# change state of game if collision occurs
def collisionCheck(player, enemies):
    if enemies:
        for enemy in enemies:
            if player.colliderect(enemy): 
                enemies.clear()
                return False
    return True

# ensure that program doesn't end unless prompted
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # close the window 'X'
            pygame.quit() # cancel the pygame module
            running = False
            exit() # leave the 'while TRUE' loop securely with sys exit
        
        if game_active: # event handler for playing state
            if event.type == pygame.KEYDOWN: # keyboard inputs
                if event.key == pygame.K_SPACE: # spacebar key
                    if toast_rect.bottom == 380: # ensure only a single jump from ground
                        toast_gravity = -16 # when pressed, send toast upwards
        
        else: # event handler for 'game over' state (reset necessary variables)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
                score = 0
                toast_rect.bottom = 380
                toast_gravity = 0
        
        if event.type == enemy_timer and game_active: # timer for enemy spawn
            if randint(0,2): # function that "randomizes" the type of enemy spawned
                enemy_list.append(egg_move_sprite.currentFrame().get_rect(center = (randint(900,1100), 250)))
            else:
                enemy_list.append(toaster_move_sprite.currentFrame().get_rect(midbottom = (randint(900,1100), 380)))
        
        if event.type == sprite_timer and game_active: # timer for sprite animation transition
            egg_move_sprite.nextFrame()
            toaster_move_sprite.nextFrame()
            toast_move_sprite.nextFrame()

    if game_active: # 'playing' state
        redrawBackground()
        screen.blit(toast_move_sprite.currentFrame(), toast_rect)

        # simulate jumping with gravity
        toast_gravity+=0.6
        toast_rect.y += toast_gravity

        enemy_list = enemyMovement(enemy_list)
        game_active = collisionCheck(toast_rect, enemy_list)

        # maintain floor for toast player
        if toast_rect.bottom >= 380: 
            toast_rect.bottom = 380
            toast_gravity = 0 # reset gravity, rather than have gravity infinitely increasing

        
    else: # 'game over' state
        screen.fill('lightslateblue')
        game_time_surface = timeTextStyle.render(f'Time: {game_time}', False, 'white') 
        game_time_rect = game_time_surface.get_rect(topleft=(150, 250))
        game_score_surface = timeTextStyle.render(f'Score: {score}', False, 'white') 
        game_score_rect = game_score_surface.get_rect(topleft=(550, 250))
        screen.blit(gg_text, gg_rect)
        screen.blit(toast_defeat_surface, toast_defeat_rect)
        screen.blit(game_time_surface, game_time_rect)
        screen.blit(game_score_surface, game_score_rect)
        screen.blit(gg_continue_text, gg_continue_rect)

    pygame.display.update() # updates the display continuously
    timer.tick(60) # ensure that while loop does not run more than 60 times per second (max frame rate)
