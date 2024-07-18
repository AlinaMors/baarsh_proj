import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 300
CARD_HEIGHT = 200
BACKGROUND_COLOR = (46, 64, 83)
CARD_COLOR = (29, 131, 72)
ANSWER_COLOR = (231, 76, 60)
TEXT_COLOR = (236, 240, 241)
BUTTON_COLOR = (93, 173, 226)
BUTTON_HOVER_COLOR = (52, 152, 219)
BUTTON_TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 24
LABEL_FONT_SIZE = 28

# Загрузка вопросов и ответов из файла
def load_flashcards(filename):
    flashcards = []
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                question = lines[i].strip()
                answer = lines[i + 1].strip()
                flashcards.append((question, answer))
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except IndexError:
        print(f"Error: The file {filename} is not properly formatted.")
    return flashcards

# Класс для карточек
class Flashcard:
    def __init__(self, question, answer, rect):
        self.question = question
        self.answer = answer
        self.rect = rect
        self.showing_question = True

    def draw(self, screen):
        color = CARD_COLOR if self.showing_question else ANSWER_COLOR
        pygame.draw.rect(screen, color, self.rect)
        font = pygame.font.Font(None, FONT_SIZE)
        label_font = pygame.font.Font(None, LABEL_FONT_SIZE)

        # Отрисовка метки "Вопрос" или "Ответ"
        label_text = "Вопрос" if self.showing_question else "Ответ"
        label_surface = label_font.render(label_text, True, TEXT_COLOR)
        label_rect = label_surface.get_rect(center=(self.rect.centerx, self.rect.top + 20))
        screen.blit(label_surface, label_rect)

        # Отрисовка основного текста
        text = self.question if self.showing_question else self.answer
        self.render_text(screen, text, font, self.rect)

    def render_text(self, screen, text, font, rect):
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            if font.size(' '.join(current_line))[0] > rect.width - 20:  # Add padding
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))

        total_height = len(lines) * font.get_height()
        text_rect = pygame.Rect(rect.left + 10, rect.top + 40, rect.width - 20, rect.height - 50)
        if total_height > text_rect.height:  # Add padding
            self.draw_scrollable_text(screen, lines, font, text_rect)
        else:
            y = text_rect.top + (text_rect.height - total_height) // 2
            for line in lines:
                text_surface = font.render(line, True, TEXT_COLOR)
                screen.blit(text_surface, (text_rect.left, y))
                y += font.get_height()

    def draw_scrollable_text(self, screen, lines, font, rect):
        # Draw scrollable area
        text_surface = pygame.Surface((rect.width, len(lines) * font.get_height()))
        text_surface.fill((255, 255, 255))
        y = 0
        for line in lines:
            line_surface = font.render(line, True, TEXT_COLOR)
            text_surface.blit(line_surface, (0, y))
            y += font.get_height()

        scroll_rect = pygame.Rect(rect.left, rect.top, rect.width, rect.height)
        screen.blit(text_surface, scroll_rect, scroll_rect)

    def flip(self):
        self.showing_question = not self.showing_question

# Класс для кнопок
class Button:
    def __init__(self, text, rect, action=None):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.action = action
        self.hovered = False

    def draw(self, screen):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def click(self):
        if self.action:
            self.action()

# Основная функция
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flashcard Game")

    flashcards = load_flashcards("flashcard_game/flashcards.txt")
    if not flashcards:
        print("No flashcards to display.")
        pygame.quit()
        sys.exit()

    current_index = 0
    current_card = Flashcard(flashcards[current_index][0], flashcards[current_index][1], pygame.Rect((SCREEN_WIDTH - CARD_WIDTH) // 2, (SCREEN_HEIGHT - CARD_HEIGHT) // 2, CARD_WIDTH, CARD_HEIGHT))

    def show_next_card():
        nonlocal current_index, current_card
        current_index = (current_index + 1) % len(flashcards)
        current_card = Flashcard(flashcards[current_index][0], flashcards[current_index][1], pygame.Rect((SCREEN_WIDTH - CARD_WIDTH) // 2, (SCREEN_HEIGHT - CARD_HEIGHT) // 2, CARD_WIDTH, CARD_HEIGHT))

    def show_previous_card():
        nonlocal current_index, current_card
        current_index = (current_index - 1) % len(flashcards)
        current_card = Flashcard(flashcards[current_index][0], flashcards[current_index][1], pygame.Rect((SCREEN_WIDTH - CARD_WIDTH) // 2, (SCREEN_HEIGHT - CARD_HEIGHT) // 2, CARD_WIDTH, CARD_HEIGHT))

    next_button = Button("Next", (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, 100, 40), show_next_card)
    prev_button = Button("Prev", (50, SCREEN_HEIGHT - 50, 100, 40), show_previous_card)

    buttons = [next_button, prev_button]

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        button.click()
                if current_card.rect.collidepoint(event.pos):
                    current_card.flip()
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.check_hover(event.pos)

        current_card.draw(screen)
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
