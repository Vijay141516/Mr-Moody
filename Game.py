# Importing Libraries
import pygame
import random

# Pygame Setup hehe
pygame.init()

# Game Settings
WIDTH = 700
HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mr Moody")

clock = pygame.time.Clock()

# Adding sprites

background = pygame.image.load("Sprites/Background.png").convert()

Moody_img = pygame.image.load("Sprites/Sprites.png").convert_alpha()

auto_img = pygame.image.load("Sprites/Riksaw.png").convert_alpha()
car_img = pygame.image.load("Sprites/Car.png").convert_alpha()
Rahul_img = pygame.image.load("Sprites/Rahul.png")
Moody_img = pygame.transform.scale(Moody_img, (120, 120))

auto_img = pygame.transform.scale(auto_img, (100, 80))
car_img = pygame.transform.scale(car_img, (140, 90))
Rahul_img = pygame.transform.scale(Rahul_img, (140, 90))

# Humare MOODY JI

player_x = 150
player_y = 500

player_width = 100
player_height = 100

velocity_y = 0
gravity = 1

jumping = False
crouching = False

GROUND_Y = 500

# Background location value
bg_x = 0

#OBSTACLES

obstacles = []
game_speed = 8

# Score System

font = pygame.font.SysFont("Arial", 40)

score = 0


def spawn_obstacle():

    obstacle_type = random.choice(["auto", "car", "Rahul"])

    if obstacle_type == "auto":
        img = auto_img
        w = 100
        h = 70

    elif obstacle_type == "car":
        img = car_img
        w = 100
        h = 70

    else:
        img = Rahul_img
        w = 100
        h = 70

    rect = pygame.Rect(
        WIDTH + 100,
        GROUND_Y + 100 - h,
        w,
        h
    )

    obstacles.append({
        "img": img,
        "rect": rect
    })


spawn_timer = 0

running = True

# GAME LOOP

while running:

    clock.tick(FPS)

    score += 1

    if score % 500 == 0:
        game_speed += 1

    # EVENTS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and not jumping:
                velocity_y = -20
                jumping = True

    keys = pygame.key.get_pressed()

    crouching = keys[pygame.K_DOWN]

    # Modi Attributes

    velocity_y += gravity
    player_y += velocity_y

    if player_y >= GROUND_Y:
        player_y = GROUND_Y
        velocity_y = 0
        jumping = False

    # SPAWN OBSTACLES

    spawn_timer += 1

    if spawn_timer > random.randint(80, 140):
        spawn_obstacle()
        spawn_timer = 0

    # MOVE OBSTACLES

    for obs in obstacles:
        obs["rect"].x -= game_speed

    obstacles = [
        obs for obs in obstacles
        if obs["rect"].right > 0
    ]

    # COLLISION

    player_rect = pygame.Rect(
        player_x,
        player_y,
        player_width,
        player_height
    )

    if crouching:
        player_rect.height = 70
        player_rect.y += 30

    for obs in obstacles:

        if player_rect.colliderect(obs["rect"]):

            game_over = True

            while game_over:

                screen.fill((0, 0, 0))

                text = font.render(
                    f"GAME OVER | SCORE: {score}",
                    True,
                    (255, 255, 255)
                )

                screen.blit(
                    text,
                    (WIDTH//2 - text.get_width()//2,
                     HEIGHT//2)
                )

                pygame.display.update()

                for e in pygame.event.get():

                    if e.type == pygame.QUIT:
                        pygame.quit()
                        quit()

    # DRAW BACKGROUND

    bg_x -= game_speed

    if bg_x <= -background.get_width():
        bg_x = 0

    screen.blit(background, (bg_x, 0))
    screen.blit(background,
                (bg_x + background.get_width(), 0))

    # DRAW Moodi ji

    player_draw = pygame.transform.scale(Moody_img,
        (120, 80 if crouching else 120))

    screen.blit(player_draw,
                (player_x, player_y))

    # DRAW OBSTACLES

    for obs in obstacles:
        screen.blit(obs["img"], obs["rect"])

    # DRAW SCORE

    score_text = font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    screen.blit(score_text, (20, 20))

    pygame.display.update()

pygame.quit()