# levels.py
import pygame
import sys
from classes import Game

pygame.init()

class NewGameWindow:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 700
        pygame.mouse.set_visible(True)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Выбор уровня")

        self.running = True

        easy_button_img = pygame.image.load("pic/btn.PNG")
        medium_button_img = pygame.image.load("pic/btn.PNG")
        hard_button_img = pygame.image.load("pic/btn.PNG")

        button_width, button_height = 150, 50
        easy_button_img = pygame.transform.scale(easy_button_img, (button_width, button_height))
        medium_button_img = pygame.transform.scale(medium_button_img, (button_width, button_height))
        hard_button_img = pygame.transform.scale(hard_button_img, (button_width, button_height))

        button_rect1 = easy_button_img.get_rect(center=(self.screen_width // 2, 150))
        button_rect2 = medium_button_img.get_rect(center=(self.screen_width // 2, 150 + button_height + 20))
        button_rect3 = hard_button_img.get_rect(center=(self.screen_width // 2, 150 + 2 * (button_height + 20)))

        self.buttons = [
            {"image": easy_button_img, "rect": button_rect1, "text": "Легкий", "settings": {"win_balls": 100, "enemy_health": 100, "hero_health": 100, "difficulty": "easy"}},
            {"image": medium_button_img, "rect": button_rect2, "text": "Средний", "settings": {"win_balls": 200, "enemy_health": 200, "hero_health": 100, "difficulty": "medium"}},
            {"image": hard_button_img, "rect": button_rect3, "text": "Трудный", "settings": {"win_balls": 300, "enemy_health": 300, "hero_health": 50, "difficulty": "hard"}},
        ]

        self.font = pygame.font.Font(None, 36)

    def run(self):
        while self.running:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button["rect"].collidepoint(mouse_x, mouse_y):
                            settings = button["settings"]
                            game = Game(win_balls=settings["win_balls"], enemy_health=settings["enemy_health"], hero_health=settings["hero_health"], difficulty=settings["difficulty"])
                            game.run()
                            self.running = False

            background_image = pygame.image.load("pic/bg_level.jpg")
            background_image = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))
            self.screen.blit(background_image, (0, 0))

            for button in self.buttons:
                self.screen.blit(button["image"], button["rect"].topleft)
                text_surface = self.font.render(button["text"], True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=button["rect"].center)
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()
