import random
import math

import pygame
from pygame import mixer

# initalinzing
pygame.init()

# creating a window
screen = pygame.display.set_mode((1400, 900))

# background image
background = pygame.image.load("bg.jpg")

#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# gametitle
pygame.display.set_caption('Galaxy shooter')
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('player.png')
playerX = 640
playerY = 740
playerX_change = 0

# enemy
enemyimg = []
enemyX =[]
enemyY=[]
enemyX_change = []
enemyY_change =[]
num_of_enemies = 6

for i in range (num_of_enemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,1272))
    enemyY.append(random.randint(10,100))
    enemyX_change.append(1)
    enemyY_change.append(100)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 740
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"

#score
score_value=0
font = pygame.font.Font("scoreboard.ttf", 50)
textX=10
textY=10

#game over
newfont= pygame.font.Font("gameover.ttf", 80)

def game_over(x,y):
    gameover = newfont.render("GAME OVER", True,(0,225,255))
    screen.blit(gameover,(450,400))

def show_score(x,y):
    score = font.render("Score : "+ str(score_value) , True ,(225,225,225))
    screen.blit(score,(x,y))

def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+48, y+20))

def iscollision(enemyX , enemyY , bulletX , bulletY):
    distance = math.sqrt((math.pow((enemyX-bulletX),2))+ (math.pow((enemyY-bulletY),2)))
    if distance < 45:
        return True
    else:
        return False

# gameloop
running = True
while running:

    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # key strokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 2.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #player movement
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 1272:
        playerX = 1272

    #enemy movement
    for i in range (num_of_enemies):

        #gameover
        if enemyY[i] >400:   
            for j in range(num_of_enemies):
                enemyY[j] =2000
                playerY =2000
            game_over(350,400)
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1272:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
         #collision
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 740
            bullet_state = "ready"
            score_value +=20
            enemyX[i] = random.randint(0, 1272)
            enemyY[i] = random.randint(10, 100)

        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY < 0:
        bulletY = 740
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
