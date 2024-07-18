import os
import sys
import pygame
from result import *

# quit func
def terminate():
    pygame.quit()
    sys.exit()

# draw bg
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, WINDOW_SIZE)
    bg_coords = (0, 0)
    screen.blit(scaled_bg, bg_coords)

# show health bar func
def show_health_bar(surface, health, x, y, total_health):
    part_of_health = health / total_health
    pygame.draw.rect(surface, (255, 0, 0), (x, y, 420, 40))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, 420 * part_of_health, 40))
    font = pygame.font.Font(None, 36)
    health_text = font.render(f'{health}/{total_health}', True, (255, 255, 255))
    surface.blit(health_text, (x + 170, y + 5))

# image load func
def load_image(name, size=None, colorkey=-1):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image

# win func
def win(winning_balls):
    resultts(winning_balls)

# lose func
def lose():
    end()

# update screen
def update(hero, enemy):
    hero.draw(screen, enemy)
    enemy.draw(screen, hero)
    draw_bg()

def show_text(surface, font, txt, x):
    text = font.render(txt, True, (150, 150, 150))
    surface.blit(text, (x, 50))

# show start screen func
def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

def handle_buttons(hero):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        hero.l_move()
    if keys[pygame.K_RIGHT]:
        hero.r_move()

# init
pygame.init()

# set size
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 700

# set FPS
FPS = 60

# make sprite group
all_sprites = pygame.sprite.Group()

# set horizontal borders
horizontal_borders = pygame.sprite.Group()

# set vertical borders
vertical_borders = pygame.sprite.Group()

# init clock
clock = pygame.time.Clock()

# create screen
screen = pygame.display.set_mode(WINDOW_SIZE)

# bg image
bg_image = pygame.image.load('pic/bg_game.gif').convert_alpha()

# enemy speed
enemy_speed = 2

# set font
font = pygame.font.Font(None, 36)
