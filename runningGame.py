# simple running game developed by Touseef Hossain
# tutorial content used in this code found from
# https://www.youtube.com/watch?v=AY9MnQ4x3zk
from time import time
import pygame
from sys import exit
from random import randint
import sprite
import toastPlayer
import runningEnemy

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 400
running = True

# window and frame settings
pygame.init() # initialize the pygame module (like starting a car with key)
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT)) # display size
pygame.display.set_caption('Toasty Run')
timer = pygame.time.Clock()
bgTextStyle = pygame.font.Font('Grand9K Pixel.ttf', 50)
timeTextStyle = pygame.font.Font('Grand9K Pixel.ttf', 20)
pygame.mixer.music.set_volume(0.7)

# change the music depending on the state of the game
def changeMusic(music):
    pygame.mixer.music.unload()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()

# 'start menu' state background settings
intro_text = bgTextStyle.render('TOASTY RUN', False, 'white')
intro_rect = intro_text.get_rect(center = (400, 80))
instr_text1 = timeTextStyle.render('Jump over obstacles', False, 'white')
instr_rect1 = instr_text1.get_rect(center = (400, 200))
instr_text2 = timeTextStyle.render('using SPACE', False, 'white')
instr_rect2 = instr_text2.get_rect(center = (400, 220))
instr_text3 = timeTextStyle.render('Press SPACE to begin', False, 'white')
instr_rect3 = instr_text3.get_rect(center = (400, 300))
changeMusic('Audio/Rivers in the Desert (8-bit).mp3')

def startMenu():
    screen.fill('skyblue3')
    screen.blit(toast_idle_sprite.currentFrame(), toast_idle_rect)
    screen.blit(intro_text, intro_rect)
    screen.blit(instr_text1, instr_rect1)
    screen.blit(instr_text2, instr_rect2)
    screen.blit(instr_text3, instr_rect3)


# 'playing' state background settings
background =  pygame.image.load('Graphics/kitchen_BG.jpg').convert()
background = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
bgX = 0
bgX2 = DISPLAY_WIDTH
bgSpeed = 2

start_time = 0 # timer that will help with maintaining accurate time whenever the game restarts
game_time = 0 # used to display total play time for a game
score = 0

# 'game over' state background settings
gg_text = bgTextStyle.render('Game Over', False, 'white')
gg_rect = gg_text.get_rect(center =(400, 80))
gg_continue_text = timeTextStyle.render('Try Again? ( SPACE )', False, 'white')
gg_continue_rect = gg_continue_text.get_rect(center = (400, 350))

toast_defeat_image = pygame.image.load('Graphics/toast_defeat.png').convert_alpha()
toast_defeat_image = pygame.transform.rotozoom(toast_defeat_image, 0, 1.6) # filter, scale, rotate
toast_defeat_image.set_colorkey('black')
toast_defeat_rect = toast_defeat_image.get_rect(center = (400, 200))

def gameOverScreen():
    screen.fill('lightslateblue')
    game_time_surface = timeTextStyle.render(f'Time: {game_time}', False, 'white') 
    game_time_rect = game_time_surface.get_rect(topleft=(150, 250))
    game_score_surface = timeTextStyle.render(f'Score: {score}', False, 'white') 
    game_score_rect = game_score_surface.get_rect(topleft=(550, 250))
    screen.blit(gg_text, gg_rect)
    screen.blit(toast_defeat_image, toast_defeat_rect)
    screen.blit(game_time_surface, game_time_rect)
    screen.blit(game_score_surface, game_score_rect)
    screen.blit(gg_continue_text, gg_continue_rect)


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

# load idle player animation for 'start menu' state
toast_idle_image = pygame.image.load('Graphics/toast_idle.png').convert_alpha()
toast_idle_sprite = sprite.Sprite(toast_idle_image, 64)
toast_idle_rect = toast_idle_sprite.currentFrame().get_rect(midbottom = (60, 380))

# load player object
player = toastPlayer.Toast()
pygame.display.set_icon(toast_idle_sprite.currentFrame()) # set window icon

# load enemy-related objects
enemy_spawn_rate = 3000
enemy_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_timer, enemy_spawn_rate)
enemy_list = []

# move the obstacles according to their respective type
def enemyMovement():
    global score, enemy_spawn_rate, bgSpeed, enemy_list
    if enemy_list:
        for enemy in enemy_list:
            enemy.move(screen)
            if enemy.outOfBounds():
                enemy_list.remove(enemy)
                score += 1
                if score%5 == 0 and enemy_spawn_rate > 600:
                    enemy_spawn_rate -= 200
                    pygame.time.set_timer(enemy_timer, enemy_spawn_rate)
                elif score%10 == 0: bgSpeed += 0.4
        return enemy_list
    else: return []

# check for collisions between player and obstacles
# change state of game if collision occurs
def collisionCheck():
    global enemy_list, player
    if enemy_list:
        for enemy in enemy_list:
            if player.getRect().colliderect(enemy.getRect()): 
                enemy_list.clear()
                changeMusic('Audio/Eterna City (Daytime) (8-bit).mp3')
                return False
    return True

game_active = True # state of the game (switch from playing and 'game over' screen)
start_menu = True # initial state of the game

# ensure that program doesn't end unless prompted
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # close the window 'X'
            pygame.quit() # cancel the pygame module
            running = False
            exit() # leave the 'while TRUE' loop securely with sys exit
        
        if start_menu:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_menu = False
                game_active = True
                changeMusic("Audio/Il Vento D'Oro (8-bit).mp3")
                start_time = pygame.time.get_ticks()

        elif not game_active: # event handler for 'game over' state (reset necessary variables)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
                score = 0
                player.reset()
                changeMusic("Audio/Il Vento D'Oro (8-bit).mp3")
        
        if event.type == enemy_timer and game_active and not start_menu: # timer for enemy spawn
            if randint(0,2): # function that "randomizes" the type of enemy spawned
                enemy_list.append(runningEnemy.Enemy('egg'))
            else:
                enemy_list.append(runningEnemy.Enemy('toaster'))
        
        if event.type == sprite_timer and start_menu: toast_idle_sprite.nextFrame()

        elif event.type == sprite_timer and game_active: # timer for sprite animation transition
            player.animate()
            for enemy in enemy_list:
                enemy.animate()

    if start_menu: # 'start menu' state
        startMenu()

    elif game_active: # 'playing' state
        redrawBackground()
        player.update(screen)
        enemy_list = enemyMovement()
        game_active = collisionCheck()

    else: # 'game over' state
        gameOverScreen()

    pygame.display.update() # updates the display continuously
    timer.tick(60) # ensure that while loop does not run more than 60 times per second (max frame rate)
