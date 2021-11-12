import pygame
import os
pygame.font.init()

WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Fighters")

WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('Roboto', 40)
WINNER_FONT = pygame.font.SysFont('Roboto', 100)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT+1
RED_HIT = pygame. USEREVENT+2

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP =  pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP =  pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def drawWindow(red, yellow, redBullets, yellowBullets, redHealth, yellowHealth):
    WIN.blit(SPACE_BACKGROUND, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    redHealthText = HEALTH_FONT.render("Health: {}".format(redHealth), 1, WHITE)
    yellowHealthText = HEALTH_FONT.render("Health: {}".format(yellowHealth), 1, WHITE)
    WIN.blit(redHealthText, (WIDTH - redHealthText.get_width() - 10, 10))
    WIN.blit(yellowHealthText,(10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in redBullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellowBullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellowHandleMovement(keysPressed, yellow):
    if keysPressed[pygame.K_a] and yellow.x - VEL > 0: #left
        yellow.x -= VEL
    if keysPressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #right
        yellow.x += VEL
    if keysPressed[pygame.K_w] and yellow.y - VEL > 0: #up
        yellow.y -= VEL
    if keysPressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 20: #down
        yellow.y += VEL

def redHandleMovement(keysPressed, red):
    if keysPressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #left
        red.x -= VEL
    if keysPressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #right
        red.x += VEL
    if keysPressed[pygame.K_UP] and red.y - VEL > 0: #up
        red.y -= VEL
    if keysPressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 20: #down
        red.y += VEL

def handleBullets(yellowBullets, redBullets, yellow, red):
    for bullet in yellowBullets:
        bullet.x += BULLET_VEL  
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellowBullets.remove(bullet)
        elif bullet.x > WIDTH - 20:
            yellowBullets.remove(bullet)

    for bullet in redBullets:
        bullet.x -= BULLET_VEL  
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            redBullets.remove(bullet)
        elif bullet.x < 20:
            redBullets.remove(bullet)

def drawWinner(text):
    drawText = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(drawText, (WIDTH//2 - drawText.get_width()//2, HEIGHT//2 - drawText.get_height()//2))
    
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    redBullets = []
    yellowBullets = []

    redHealth, yellowHealth = 10, 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellowBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
                    yellowBullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(redBullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
                    redBullets.append(bullet)
            
            if event.type == RED_HIT:
                redHealth -= 1

            if event.type == YELLOW_HIT:
                yellowHealth -= 1

        winnerText = ""
        if redHealth <= 0:
            winnerText = "Yellow Wins!"
        if yellowHealth <= 0:
            winnerText = "Red Wins!"
        if winnerText != "":
            drawWinner(winnerText)
            break
        
        keysPressed = pygame.key.get_pressed()
        yellowHandleMovement(keysPressed, yellow)
        redHandleMovement(keysPressed, red)

        handleBullets(yellowBullets,redBullets, yellow, red)


        drawWindow(red, yellow, redBullets, yellowBullets, redHealth, yellowHealth)
    
    main()

if __name__ == "__main__":
    main()
