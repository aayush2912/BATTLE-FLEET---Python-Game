import pygame
import random
import math
from pygame import mixer

# intialize the pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))
done = True

# applying background
background = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

# setting up title and icon
pygame.display.set_caption("Battle Fleet")
icon = pygame.image.load('battleship.png')
pygame.display.set_icon(icon)

# setting up player
player_icon = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# setting up enemy
enemy_icon = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemy = 6
for i in range(number_of_enemy):
    enemy_icon.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# setting up bullet
bullet_icon = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 4
bulletY_change = 10
bullet_state = "loaded"

# count the score
score_value = 0
textX = 10
textY = 10

# print Score
font = pygame.font.Font('freesansbold.ttf', 32)

# print Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


# display spaceship on screen
def player(x, y):
    screen.blit(player_icon, (x, y))


# display enemy on screen
def enemy(x, y, i):
    screen.blit(enemy_icon[i], (x, y))


# to fire bulletss
def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_icon, (x + 16, y + 10))


# to detect collission
def collission(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if dist < 27:
        return True
    else:
        return False


# to display score
def score(x, y):
    text = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(text, (x, y))


# to display Game Over
def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# game loop
while done:
    # setting background color
    screen.fill((0, 0, 45))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # quit option enable
        if event.type == pygame.QUIT:
            done = False

        # check what key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "loaded":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # setting up boundaries for player
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # setting up boundaries for enemy
    for i in range(number_of_enemy):
        # condition for Game Over
        if enemyY[i] > 440:
            for j in range(number_of_enemy):
                enemyY[j] = 5000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # checking for collission
        isCollission = collission(enemyX[i], enemyY[i], bulletX, bulletY)
        if isCollission:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "loaded"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # placing enemy on screen
        enemy(enemyX[i], enemyY[i], i)

    # setting up bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "loaded"
    if bullet_state is "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # placing spaceship on screen
    player(playerX, playerY)

    # displaying score at top corner
    score(textX, textY)
    pygame.display.update()