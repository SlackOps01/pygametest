import pygame
import random
import math

pygame.init()
score_value = 0
font = pygame.font.Font('Roboto-Bold.ttf', 32)
textX = 10
textY = 10

back_drop  = ["back.jpg", "back2.jpg", "back3.jpg"]
over_font = pygame.font.Font('Roboto-Bold.ttf', 64)
pygame.display.set_caption("Lanre is the absolute best")
icon = pygame.image.load('ufo.png')
background = pygame.image.load(random.choice(back_drop))
background = pygame.transform.scale(background, (800, 600))
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 600))

playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 20
for i in range(num_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 200))
    enemyX_change.append(1)
    enemyY_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.5
bullet_state = "ready"


def show_score(x, y):
    score = font.render(f"Score : {str(score_value)}", True, (255, 255, 0))
    screen.blit(score, (x, y))


def over():
    over_text = font.render(f"GAME OVER", True, (255, 255, 0))
    screen.blit(over_text, (300, 250))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True

while running:
    screen.fill((255, 255, 0))
    screen.blit(background, (0, 0))
    show_score(textX, textY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -1.5
                print("key left was pressed")
            if event.key == pygame.K_d:
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0
                print(playerX)

    playerX += playerX_change
    enemyX += enemyX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_enemies):
        if enemyY[i] >= playerY:
            over()
            for j in range(num_enemies):
                enemyY[i] = 2000
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            if bulletX == playerX and bulletY == playerY:
                pass
            else:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                print(score_value)
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 400)
        enemy(enemyX[i], enemyY[i], i)
    player(playerX, playerY)


    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    pygame.display.update()
