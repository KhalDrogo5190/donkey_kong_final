#Anders Blom
#Super Gnarly Code


# Imports
import pygame
import ctypes
import time
import random
import math

# Defaults
shot_fired = False
raining = False

# Instructions
while True:
    ctypes.windll.user32.MessageBoxW(0, "W = shoot, A = left, D = right, R = toggle rain.", "Commands", 1)
    time.sleep(0.5)
    break

# Initialize game engine
pygame.mixer.pre_init()
pygame.init()

#Images
sky = pygame.image.load('photos/dk_sky_2.png')
ground = pygame.image.load('photos/dk_ground.png')
barrel = pygame.image.load('photos/barrel_rotate.png')
donkey_kong = pygame.image.load('photos/donkey_kong.png')
banana_bunch = pygame.image.load('photos/banana_bunch.png')

# Window
SIZE = (1300, 650)
TITLE = "Donkey Kong Shooter"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED =(255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (255,125,0)
BROWN = (139,69,19)
GREY = (196, 190, 186)
DARK_BLUE = (0, 0, 100)
GREY2 = (141,135,141)
SPACE_GREEN = (83, 155, 85)
YELLOW = (255, 255, 200)


#character 
character_loc = [380, 460]
vel = [0, 0]
speed = 20

#drawings
def draw_character(loc):
    x = character_loc[0]
    y = character_loc[1]
    
    screen.blit(donkey_kong, (x, y))
    
def draw_bullet(loc):
    x = loc[0]
    y = loc[1]

    screen.blit(banana_bunch, (x,y))

def draw_barrel(l):
    x = l[0]
    y = l[1]

    screen.blit(barrel, (x, y))

def draw_sky(sky):
    screen.fill(BLACK)
    screen.blit(sky, (0, -150))
    
def draw_ground(ground) :
    screen.blit(ground, (-5,450))

def draw_raindrop(drop):
    rect = drop[:4]
    pygame.draw.ellipse(screen, DARK_BLUE, rect)


#lists
bullets = []
barrels = []
rain = []

#make list of barrels
for i in range(5):
    x = random.randrange(1,1200)
    y = random.randrange(-500,-100)
    l = [x,y]
    barrels.append(l)

def make_list_rain():
    #make list of rain
    num_drops = 700

    for i in range(num_drops):
        x = random.randrange(0, 1300)
        y = random.randrange(-100, 600)
        r = random.randrange(1, 5)
        stop = random.randrange(400, 700)
        drop = [x, y, r, r, stop]
        rain.append(drop)
            
    

# Sound Effects
pygame.mixer.music.load("sounds/rain.ogg")


# Game loop


done = False

while not done:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                vel[0] = speed
            if event.key == pygame.K_a:
                vel[0] =-1 *  speed
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                vel[0] = 0
            if event.key == pygame.K_a:
                vel[0] = 0
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    shot_fired = True
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if raining == True:
                        raining = False
                        pygame.mixer.music.pause()
                    else:
                        raining = True
                        make_list_rain()
                        pygame.mixer.music.play(1)
    #Game logic
        
    #move block
    character_loc[0] += vel[0]
    
    if character_loc[0] < -164:
        character_loc[0] = 1310
    if character_loc[0] > 1310:
        character_loc[0] = -164
    
    #move bullet
    if shot_fired == True:
        bullets.append([character_loc[0] + 17.5, character_loc[1]])
        shot_fired = False
        
    for b in bullets:
        b[1] -= 24

    bullets = [b for b in bullets if b[1] > -100]
    

    #move barrels
    for l in barrels:
        l[1] += 1

        if l[1] > 651:
            
            l[1] = random.randrange(-500,-150)
            
    #move rain
    if raining:
        for r in rain:
            r[0] -= 1
            r[1] += 4

            if r[1] > r[4]:
                r[0] = random.randrange(0, 1400)
                r[1] = random.randrange(-100, 0)
    if not raining:
        rain = [r for r in rain if r[1] < 0]
            
    # Drawing code
    '''screen'''
    draw_sky(sky)
    
    ''' rain ''' 
    for r in rain:
        draw_raindrop(r)
        
    '''ground'''
    draw_ground(ground)

    '''barrels'''
    for l in barrels:
        draw_barrel(l)

    '''character'''
    draw_character(character_loc)

    '''bullets'''
    for b in bullets:
        draw_bullet(b)

        
    # Update screen
    pygame.display.flip()
    clock.tick(refresh_rate)

# Close window on quit
pygame.quit()
