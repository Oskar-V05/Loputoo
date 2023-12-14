import pygame
import sys
import random
import time

pygame.init()     #Süsteem

# Kindlad piirangud, mis ei muutu
WIDTH, HEIGHT = 800, 600  
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Pildi loomine
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

#Mängija ja arvuti reketid ning pall
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)

#Algne palli kiirus
ball_speed = [4, 4]

#Mängija ja arvuti punktid
player_score = 0
opponent_score = 0

#Arvuti reketi liikumiskiirus ja ta reaktsiooniaeg
opponent_speed = 3
opponent_reaction_time = 10 

#Font, millega näidatakse mänguseisu
font = pygame.font.Font(None, 36)

#Punkti saamisel restartimise tingimuse
restart_game = False
restart_countdown = 3
restart_timer = time.time()

#Mängutsükkel
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0: #kui vajutada noolt üles, siis liigub mängija reket üles
        player_paddle.y -= 5
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:    #kui vajutada noolt alla, siis liigub mängija reket alla
        player_paddle.y += 5

    if not restart_game:
        #Palli liikumine
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        #Palli põrkumine seintega
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        #Palli põrkumine reketitega
        if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
            ball_speed[0] = -ball_speed[0]

            #Palli kiiruse suurenemine peale igat reketi põrget
            ball_speed[0] += 1
            ball_speed[1] += 2

        #Vastase reaktsiooniaeg võrreldes palliga
        if opponent_paddle.centery < ball.centery - opponent_reaction_time:
            opponent_paddle.y += 7
        elif opponent_paddle.centery > ball.centery + opponent_reaction_time:
            opponent_paddle.y -= 7

        #Kontrollib kas pall tabab paremat või vasakut külge ja lisab punkti õigele poolele
        if ball.left <= 0:
            opponent_score += 1
            restart_game = True
        elif ball.right >= WIDTH:
            player_score += 1
            restart_game = True

    else:
        #Taimer enne kui mäng teeb restarti
        if time.time() - restart_timer >= 1:
            restart_countdown -= 1
            restart_timer = time.time()

        if restart_countdown == 0:
            restart_game = False
            ball.x = WIDTH // 2 - BALL_RADIUS // 2
            ball.y = HEIGHT // 2 - BALL_RADIUS // 2
            ball_speed = [4, 4]  #Paneb palli kiiruse ja asukoha uuesti originaalseks pärast restarti
            restart_countdown = 3

    #Tekitab need detailid ekraanile
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    #Tekitab puhktitabeli
    score_text = font.render(f"{player_score} - {opponent_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    #Tekitab restarti loenduri
    if restart_game:
        countdown_text = font.render(str(restart_countdown), True, WHITE)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))

    #Uuendab ekraani
    pygame.display.flip()

    #Määrab kindla kaadrisageduse
    clock.tick(FPS)