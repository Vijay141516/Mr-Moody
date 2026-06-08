# Importing Libraries
import pygame
import random

# Pygame Setup hehe
pygame.init()
try:
    pygame.mixer.init()
    jump_sound = pygame.mixer.Sound("jump.wav")
    crash_sound = pygame.mixer.Sound("crash.wav")
except:
    jump_sound = None
    crash_sound = None

def play_sound(snd):
    if snd:
        snd.play()

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
small_font = pygame.font.SysFont("Arial", 30)

score = 0

def reset_game():
    global score, game_speed, obstacles, player_y, velocity_y, jumping, crouching, spawn_timer, bg_x
    score = 0
    game_speed = 8
    obstacles = []
    player_y = GROUND_Y
    velocity_y = 0
    jumping = False
    crouching = False
    spawn_timer = 0
    bg_x = 0

STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAMEOVER = 3

current_state = STATE_MENU


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

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if current_state == STATE_MENU:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    current_state = STATE_PLAYING
            
            elif current_state == STATE_PLAYING:
                if event.key == pygame.K_ESCAPE:
                    current_state = STATE_PAUSED
                elif event.key == pygame.K_SPACE and not jumping:
                    velocity_y = -20
                    jumping = True
                    play_sound(jump_sound)

            elif current_state == STATE_PAUSED:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    current_state = STATE_PLAYING
                elif event.key == pygame.K_m:
                    current_state = STATE_MENU
            
            elif current_state == STATE_GAMEOVER:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    current_state = STATE_PLAYING
                elif event.key == pygame.K_m:
                    current_state = STATE_MENU

    if current_state == STATE_MENU:
        screen.fill((0, 0, 0))
        title_text = font.render("MR MOODY", True, (255, 255, 0))
        start_text = small_font.render("Press ENTER to Play", True, (255, 255, 255))
        
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
        pygame.display.update()
        continue

    elif current_state == STATE_PAUSED:
        screen.fill((0, 0, 0))
        pause_text = font.render("PAUSED", True, (255, 255, 0))
        resume_text = small_font.render("Press ESC or ENTER to Resume", True, (255, 255, 255))
        menu_text = small_font.render("Press M for Main Menu", True, (255, 255, 255))
        
        screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//3))
        screen.blit(resume_text, (WIDTH//2 - resume_text.get_width()//2, HEIGHT//2))
        screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 + 50))
        pygame.display.update()
        continue

    elif current_state == STATE_GAMEOVER:
        screen.fill((0, 0, 0))
        gameover_text = font.render("GAME OVER", True, (255, 0, 0))
        score_text_go = font.render(f"SCORE: {score}", True, (255, 255, 255))
        restart_text = small_font.render("Press ENTER to Restart", True, (255, 255, 255))
        menu_text = small_font.render("Press M for Main Menu", True, (255, 255, 255))
        
        screen.blit(gameover_text, (WIDTH//2 - gameover_text.get_width()//2, HEIGHT//3 - 30))
        screen.blit(score_text_go, (WIDTH//2 - score_text_go.get_width()//2, HEIGHT//3 + 20))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 30))
        screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 + 80))
        pygame.display.update()
        continue

    # PLAYING STATE
    score += 1

    if score % 500 == 0:
        game_speed += 1

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
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    if crouching:
        player_rect.height = 70
        player_rect.y += 30

    for obs in obstacles:
        if player_rect.colliderect(obs["rect"]):
            if current_state != STATE_GAMEOVER:
                play_sound(crash_sound)
            current_state = STATE_GAMEOVER

    # DRAW BACKGROUND
    bg_x -= game_speed
    if bg_x <= -background.get_width():
        bg_x = 0

    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x + background.get_width(), 0))

    # DRAW Moodi ji
    import math
    tilt_angle = 0
    y_offset = 0

    if jumping:
        tilt_angle = -15
    elif crouching:
        tilt_angle = 15
    else:
        # Running animation (bobbing and tilting)
        tilt_angle = math.sin(pygame.time.get_ticks() * 0.015) * 12
        y_offset = abs(math.sin(pygame.time.get_ticks() * 0.015)) * 10

    player_draw = pygame.transform.scale(Moody_img, (120, 80 if crouching else 120))
    player_draw = pygame.transform.rotate(player_draw, tilt_angle)
    
    # Get the new rect to keep the image centered while rotating
    draw_rect = player_draw.get_rect(center=(player_x + 60, player_y + (40 if crouching else 60) - y_offset))
    
    screen.blit(player_draw, draw_rect.topleft)

    # DRAW OBSTACLES
    for obs in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obs["rect"], 3)
        screen.blit(obs["img"], obs["rect"])

    # DRAW SCORE
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    pygame.display.update()

pygame.quit()