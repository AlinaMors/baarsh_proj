import pygame
import sys
import os
from pygame import mixer
from levels import NewGameWindow

pygame.init()
mixer.init()
screen_width = 1210
screen_height = 705
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Меню")

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

def button_draw(where, color, is_used_color, x, y, width, height, text, color_text):
    rect_x = width / 2
    rect_y = height / 2
    rect_meaures = (width, height)
    button_rect = pygame.Rect(x - rect_x, y - rect_y, *rect_meaures)
    is_used = button_rect.collidepoint(pygame.mouse.get_pos())
    change_color = is_used_color if is_used else color
    pygame.draw.rect(where, change_color, (x - rect_x, y - rect_y, *rect_meaures))
    pygame.draw.rect(where, (229, 94, 88), (x - rect_x, y - rect_y, width, height // 2))

    pygame.draw.line(where, (0, 0, 0), (x - rect_x + 2, y + rect_y - 2), (x + rect_x - 2, y + rect_y - 2), 4)
    pygame.draw.line(where, (0, 0, 0), (x + rect_x - 2, y - rect_y + 2), (x + rect_x - 2, y + rect_y - 2), 4)
    pygame.draw.line(where, (0, 0, 0), (x - rect_x + 2, y - rect_y + 2), (x + rect_x - 2, y - rect_y + 2), 4)
    pygame.draw.line(where, (0, 0, 0), (x - rect_x + 2, y - rect_y + 2), (x - rect_x + 2, y + rect_y - 2), 4)

    text_where = font.render(text, True, color_text)
    text_rect = text_where.get_rect(center=(x, y))
    where.blit(text_where, text_rect)

background_image = pygame.image.load("pic/bg_naruto1.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

font = pygame.font.Font(None, 36)

class SettingsWindow:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load("pic/bg_settings.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))

        self.music_playing = False
        self.returned_to_menu = False

    def run(self):
        button_spacing = 30
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    btn_rect1 = pygame.Rect(screen_width // 2 - 90, 300 - 25, 200, 50)
                    btn_rect2 = pygame.Rect(screen_width // 2 - 90, 400, 170, 30)

                    if btn_rect1.collidepoint(mouse_x, mouse_y):
                        self.toggle_music()
                    elif btn_rect2.collidepoint(mouse_x, mouse_y):
                        self.go_back_to_menu()

            self.screen.blit(self.background_image, (0, 0))

            sound_button_color = ('#d9342b' if not self.music_playing else '#00FF00')
            back_button_color = '#cc1b00'

            button_draw(self.screen, sound_button_color, '#FFBA00', screen_width // 2, 300, 200, 
                        50, 'Звук', '#FFFDD0')

            button_draw(self.screen, back_button_color, '#380101', screen_width // 2, 400, 
                        170, 30, 'Назад', (255, 255, 255))

            mouse()

            pygame.display.flip()
            clock.tick(60)

            if self.returned_to_menu:
                running = False

    def toggle_music(self):
        music_file = 'pic/grey_night.mp3'
        if not self.music_playing:
            try:
                mixer.music.load(music_file)
                mixer.music.play()
                self.music_playing = True
            except pygame.error as e:
                print(f"Error loading music: {e}")
        else:
            mixer.music.stop()
            self.music_playing = False

    def go_back_to_menu(self):
        self.returned_to_menu = True

def mouse():
    cursor_image = load_image('pic/mouse_cursor.jpg', (50, 50))
    pygame.mouse.set_visible(False)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(cursor_image, (mouse_x - cursor_image.get_width() // 2, mouse_y - cursor_image.get_height() // 2))

class MainMenu:
    def __init__(self):
        self.background_image = pygame.image.load("pic/bg_naruto1.png")
        self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))
        self.running = True

    def run(self):
        while self.running:
            words = ['Новая игра', 'Настройки', 'Выйти']
            button_spacing = 70
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    button_rect1 = pygame.Rect(screen_width // 2 - 100, 200 - 25, 200, 50)
                    button_rect2 = pygame.Rect(screen_width // 2 - 100, 200 + button_spacing - 25, 200, 50)
                    button_rect3 = pygame.Rect(screen_width // 2 - 100, 200 + 2 * button_spacing - 25, 200, 50)

                    if button_rect1.collidepoint(mouse_x, mouse_y):
                        new_game_window = NewGameWindow()
                        new_game_window.run()
                    elif button_rect2.collidepoint(mouse_x, mouse_y):
                        settings_window = SettingsWindow(screen)
                        settings_window.run()
                        if settings_window.returned_to_menu:
                            continue  # If settings window returns to menu, continue the main loop
                    elif button_rect3.collidepoint(mouse_x, mouse_y):
                        self.running = False

            screen.blit(self.background_image, (0, 0))
            button_draw(screen, ('#d9342b'), ('#FFBA00'), screen_width // 2, 200, 200, 50, words[0], ('#FFFDD0'))
            button_draw(screen, ('#d9342b'), ('#FFBA00'), screen_width // 2, 200 + button_spacing, 200, 50, words[1], ('#FFFDD0'))
            button_draw(screen, ('#d9342b'), ('#FFBA00'), screen_width // 2, 200 + 2 * button_spacing, 200, 50, words[2], ('#FFFDD0'))

            mouse()
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()
