import pygame
import os
import sys

class ResultButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('pic/btn.PNG')
        self.rect = self.image.get_rect(center=(600, 550))
        self.font = pygame.font.Font(None, 36)
        self.text = 'Закончить'
        self.rendered_text = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def update_text(self, new_text):
        self.text = new_text
        self.rendered_text = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def is_clicked(self):
        return end()

def end():
    pygame.init()
    all_sprites = pygame.sprite.Group()
    result_button = ResultButton()
    all_sprites.add(result_button)

    screen = pygame.display.set_mode((1200, 700))
    pygame.display.set_caption("Game over")

    clock = pygame.time.Clock()
    dt = 0  # Инициализация прошедшего времени

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = clock.tick(60)  # Получаем прошедшее время с момента последнего вызова
        all_sprites.update(dt)  # Вызываем метод update для всех спрайтов

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        # Display "вы проиграли" text
        font = pygame.font.Font(None, 74)
        text_surface = font.render("ВЫ ПРОИГРАЛИ", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(600, 350))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()
