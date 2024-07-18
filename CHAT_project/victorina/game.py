import pygame
import sqlite3
import time

# Настройки игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 36
QUESTION_FONT_SIZE = 48  # Увеличенный размер шрифта для вопроса
TIMER_FONT_SIZE = 48  # Увеличенный размер шрифта для таймера
TIME_EASY = 30
TIME_HARD = 15
POINTS_EASY = 10
POINTS_HARD = 20
ANSWER_BOX_WIDTH = 700
ANSWER_BOX_HEIGHT = 50

class QuizGame:
    def __init__(self):
        self.conn = sqlite3.connect('quiz.db')
        self.cursor = self.conn.cursor()

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Quiz Game')

        self.font = pygame.font.Font(None, FONT_SIZE)
        self.question_font = pygame.font.Font(None, QUESTION_FONT_SIZE)  # Шрифт для вопроса
        self.timer_font = pygame.font.Font(None, TIMER_FONT_SIZE)  # Шрифт для таймера
        self.small_font = pygame.font.Font(None, 28)
        self.answer_box_rects = []

        self.background = pygame.image.load('victorina/4.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def load_quiz(self, quiz_id):
        self.cursor.execute("SELECT * FROM questions WHERE quiz_id=?", (quiz_id,))
        self.questions = self.cursor.fetchall()
        self.current_question = 0
        self.score = 0
        self.time_left = TIME_EASY if self.questions[0][5] == 'easy' else TIME_HARD
        self.answer_input = ''

    def display_question(self):
        question = self.questions[self.current_question]
        question_text = question[2]
        options = question[3].split(',')
        self.correct_option = question[4]

        self.screen.blit(self.background, (0, 0))

        # Отображение вопроса
        question_surf = self.question_font.render(question_text, True, (255, 255, 255))
        question_rect = question_surf.get_rect(center=(SCREEN_WIDTH//2, 80))
        pygame.draw.rect(self.screen, (0, 0, 0), question_rect.inflate(20, 20))  # Рамка вокруг вопроса
        self.screen.blit(question_surf, question_rect)

        mouse_pos = pygame.mouse.get_pos()

        self.answer_box_rects = []
        for i, option in enumerate(options):
            rect = pygame.Rect(50, 200 + i * 70, ANSWER_BOX_WIDTH, ANSWER_BOX_HEIGHT)
            self.answer_box_rects.append(rect)

            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (100, 100, 255), rect)
            else:
                pygame.draw.rect(self.screen, (200, 200, 200), rect)

            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            option_surf = self.font.render(f"{i+1}. {option}", True, (0, 0, 0))
            self.screen.blit(option_surf, (rect.x + 10, rect.y + 10))

        # Отображение таймера
        timer_surf = self.timer_font.render(f"Time left: {int(self.time_left)}s", True, (255, 0, 0))
        timer_rect = timer_surf.get_rect(center=(SCREEN_WIDTH//2, 150))
        pygame.draw.rect(self.screen, (255, 255, 255), timer_rect.inflate(20, 20))  # Фон для таймера
        self.screen.blit(timer_surf, timer_rect)

        input_box_surf = self.small_font.render(self.answer_input, True, (0, 0, 0))
        input_box_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, ANSWER_BOX_WIDTH, ANSWER_BOX_HEIGHT)
        pygame.draw.rect(self.screen, (255, 255, 255), input_box_rect)
        self.screen.blit(input_box_surf, (input_box_rect.x + 5, input_box_rect.y + 5))

        pygame.display.flip()

    def display_feedback(self, correct):
        feedback_color = (0, 255, 0) if correct else (255, 0, 0)
        feedback_text = "Correct!" if correct else "Wrong!"

        self.screen.blit(self.background, (0, 0))
        feedback_surf = self.font.render(feedback_text, True, feedback_color)
        self.screen.blit(feedback_surf, (350, 250))
        pygame.display.flip()
        time.sleep(1)

    def check_answer(self, selected_option):
        question = self.questions[self.current_question]
        options = question[3].split(',')

        if selected_option == self.correct_option or options[selected_option] == self.correct_option:
            self.score += POINTS_EASY if question[5] == 'easy' else POINTS_HARD
            self.display_feedback(True)
        else:
            self.display_feedback(False)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.display_question()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(self.answer_box_rects):
                        if rect.collidepoint(event.pos):
                            self.check_answer(i)
                            self.current_question += 1
                            if self.current_question >= len(self.questions):
                                running = False
                            else:
                                self.time_left = TIME_EASY if self.questions[self.current_question][5] == 'easy' else TIME_HARD
                            break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.check_answer(self.answer_input.strip())
                        self.answer_input = ''
                        self.current_question += 1
                        if self.current_question >= len(self.questions):
                            running = False
                        else:
                            self.time_left = TIME_EASY if self.questions[self.current_question][5] == 'easy' else TIME_HARD
                    elif event.key == pygame.K_BACKSPACE:
                        self.answer_input = self.answer_input[:-1]
                    else:
                        self.answer_input += event.unicode

            self.time_left -= clock.tick(30) / 1000.0
            if self.time_left <= 0:
                self.display_feedback(False)
                self.current_question += 1
                if self.current_question >= len(self.questions):
                    running = False
                else:
                    self.time_left = TIME_EASY if self.questions[self.current_question][5] == 'easy' else TIME_HARD

        self.display_result()
        time.sleep(3)
        pygame.quit()

    def display_result(self):
        self.screen.fill((255, 255, 255))
        result_surf = self.font.render(f"Your score: {self.score}", True, (0, 0, 0))
        self.screen.blit(result_surf, (350, 250))
        pygame.display.flip()

quiz_game = QuizGame()
quiz_game.load_quiz(1)  # Загрузите викторину с идентификатором 1
quiz_game.run()
