# Imports
import pygame
import math
import random

pygame.init()

        
# Window
WIDTH = 800
HEIGHT = 600
TITLE = "Bird Hunt"
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

#Initialization
bird_x = 0
bird_y = 0
initial_x = 0
initial_y = 0
target_x = 400
target_y = 300
skin = 1
bird_rate = 250
time = 0
score = 0
high_score = 0
ammo = 100
misses = 5
dead_bird = False #Determines whether the current bird is dead
held = False #Determines whether the player is holding down the mouse button
my_font = pygame.font.SysFont("Times New Roman", 24)
cursor = pygame.cursors.compile(pygame.cursors.textmarker_strings)
pygame.mouse.set_cursor(*pygame.cursors.broken_x)



#Helper Functions--------------------------------------------

#Creates a gradient
def gradient_maker(start,end):
    for y in range(HEIGHT):
        r = int(start[0] + (end[0] - start[0]) * y / HEIGHT)
        g = int(start[1] + (end[1] - start[1]) * y / HEIGHT)
        b = int(start[2] + (end[2] - start[2]) * y / HEIGHT)

        pygame.draw.line(screen, [r, g, b], [0, y], [WIDTH, y])
#Draws a bird
def draw_bird(x,y,skin):
    bird = pygame.image.load("images/bird" + str(skin) + ".png").convert_alpha()
    screen.blit(bird, [x, y])

#Displays Text
def create_label(text,x,y,color):
    label = my_font.render(text, 1, color)
    screen.blit(label, (x,y))

#Determines How The Bird Will Move After It Is Spawned
def create_bird(direction):
    global bird_x, bird_y, initial_x, initial_y, target_x, target_y
    if direction <= 800:
        bird_x = direction-15
        bird_y = -15
    elif direction <= 1400:
        bird_x = 785
        bird_y = direction - 815
    elif direction <= 2200:
        bird_x = direction - 1415
        bird_y = 585
    else:
        bird_x = -15
        bird_y = 2785-direction
    initial_x = bird_x
    initial_y = bird_y
    target_x = random.randint(300,500)
    target_y = random.randint(200,400)
        
#Detects if the bird is hit
def hit_check():
    global ammo, bird_rate, score, high_score, dead_bird, bird_x, bird_y
    ammo -= 1
    if 0 <= pygame.mouse.get_pos()[0] - bird_x <= 32 and 0 <= pygame.mouse.get_pos()[1] - bird_y <= 32:
        if dead_bird == False:
            bird_rate *= .95
            bird_rate = int(bird_rate)
            score += 1
            if score > high_score:
                high_score += 1
            dead_bird = True

#Allows the player to reset the game or quit it          
def end_game():
    global ammo, bird_rate,misses,dead_bird,bird_y,score
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ammo = 100
                bird_rate = 250
                misses = 5                  
                dead_bird = True
                bird_y = 1000
                score = 0
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                exit()
    
# Game loop
done = False

#Initial Drawings


while not done:
    # Event processing 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True     

    #Game Logic--------------------------------------------------

    #Hit Detection
    if (event.type == pygame.MOUSEBUTTONDOWN and ammo > 0):
        if held == False:
            held = True
            hit_check()
    else:
        held = False
            
    #Add Bird
    if (bird_x < -20) or (bird_x > 820) or (bird_y < -20) or (bird_y > 620):
        
        if dead_bird == False:
            misses -= 1
            
        dead_bird = False

        skin = random.randint(1,5)       
        direction = random.randint(0,2800)
        create_bird(direction)


   #Bird Movement     
    if dead_bird:   
        vx = 0
        vy = 7
    else:
        vx = (target_x-initial_x)/bird_rate
        vy = (target_y-initial_y)/bird_rate

    bird_x += 2*vx
    bird_y += 2*vy

    


    #Sky Processing---------------------------------------------------
    
    #background brightness
    day_length = 120000
    brightness = abs(day_length/2-(pygame.time.get_ticks()%day_length))
    brightness /= (day_length/512)
    brightness = int(brightness)

    #top of gradient
    top = (0,brightness/2,brightness)

    #bottom of gradient
    horizon_blue = int(abs(128-brightness)*2)
    if horizon_blue < 0:
        horizon_blue = 0
    
    horizon_red = brightness *2
    if horizon_red > 255:
        horizon_red = 255
    horizon = (horizon_red,brightness,horizon_blue)

    #Colors
    brightness = float(brightness)
    grass = (0,brightness/1.5,0)
    trunk = (brightness/2,brightness/4,0)
    leaf = (0,brightness/2,0)
    black = (0,0,0)
    white = (255,255,255)
    blue = (0,0,255)
    red = (255,0,0)

    #Drawing code---------------------------------------------------
    
    gradient_maker(top,horizon) #draws sky


    #Draw bird
    draw_bird(bird_x,bird_y,skin)
        
    #Adds foreground elements
    pygame.draw.rect(screen, grass, [0,500,800,400])
    pygame.draw.rect(screen, trunk, [0,0,50,500])
    pygame.draw.rect(screen, trunk, [750,0,50,500])
    for x in range (0,8):
        pygame.draw.ellipse(screen, leaf, [(100*x)-50,-50,200,100])
    create_label("Score: " + str(score),10,7,white)
    create_label("High Score: " + str(high_score),650,7,white)
    create_label("Ammo: " + str(ammo),10,550,blue)
    create_label("Misses: " + str(misses) + "/5",650,550,red)

    #End Game
    if ammo == 0 or misses == 0:
        pygame.draw.rect(screen, black, [0,0,800,600])
        create_label("YOUR SCORE: " + str(score),300,150,white)
        create_label("HIGH SCORE: " + str(high_score),300,250,white)
        create_label("Press Space to Play Again", 270, 450, white)
        create_label("Press Enter to Quit", 300, 480, white)


    # Update screen-------------------------------------------------
    pygame.display.flip()
    clock.tick(refresh_rate)

    #End Game-------------------------------------------------------
    if ammo == 0 or misses == 0:
        end_game()

                
# Close window on quit
pygame.quit()
