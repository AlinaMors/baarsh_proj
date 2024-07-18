import sys
import pygame
import pygame_gui
from functions import *
from time import time
from questions import Question


def show_health_bar(surface, health, x, y, total_health, label):
    part_of_health = health / total_health
    pygame.draw.rect(surface, (255, 0, 0), (x, y, 420, 40))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, 420 * part_of_health, 40))
    font = pygame.font.Font(None, 36)
    health_text = font.render(f'{health}/{total_health}', True, (255, 255, 255))
    surface.blit(health_text, (x + 170, y + 5))

    # Draw label below the health bar
    label_text = font.render(label, True, (255, 255, 255))
    surface.blit(label_text, (x, y + 45))


class Game:
    def __init__(self, win_balls=100, enemy_health=100, hero_health=100, difficulty="easy"):
        self.manager = pygame_gui.UIManager(WINDOW_SIZE)
        self.hero = Hero(100, 410, hero_health, win_balls, self.manager, self)
        self.enemy = Enemy(700, 410, enemy_speed, enemy_health, difficulty)
        pygame.display.set_caption('Game')
        
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

    def run(self):
        while self.running:
            time_delta = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.USEREVENT:
                    if hasattr(event, 'user_type') and event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.hero.submit_button:
                        answer = self.hero.answer_entry.get_text()
                        self.hero.answer_question(answer, self.enemy)
                        self.manager.get_root_container().enable()

                self.manager.process_events(event)

            if not self.paused:
                self.hero.handle_input()
                self.hero.update()
                self.enemy.update(self.hero)

                # Check for game over
                if self.hero.health <= 0 or self.enemy.health <= 0 or not self.hero.question.has_more_questions():
                    self.running = False

            self.manager.update(time_delta)

            draw_bg()
            self.enemy.draw(screen, self.hero)
            self.hero.draw(screen, self.enemy)
            self.manager.draw_ui(screen)
            
            # Show health bars with labels
            show_health_bar(screen, self.hero.health, 50, 50, self.hero.total_health, "Ваша жизнь")
            show_health_bar(screen, self.enemy.health, 700, 50, self.enemy.total_health, "Жизнь учителя-сенсея")

            pygame.display.flip()

        if self.hero.health <= 0:
            self.hero.is_dead = True
        if self.enemy.health <= 0:
            self.enemy.is_dead = True

        self.show_game_over()

    def show_game_over(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill((0, 0, 0))

            if self.hero.is_dead or self.hero.health < self.enemy.health:
                winner_text = "ENEMY WINS"
                self.enemy.draw_dead(screen)
            elif self.enemy.is_dead or self.hero.health > self.enemy.health:
                winner_text = "HERO WINS"
                self.hero.draw_dead(screen)
            else:
                winner_text = "DRAW"
                self.hero.draw_dead(screen)
                self.enemy.draw_dead(screen)

            font = pygame.font.Font(None, 74)
            text_surface = font.render(winner_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(600, 350))
            screen.blit(text_surface, text_rect)

            pygame.display.flip()
            clock.tick(FPS)

class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, health, win_balls, manager, game):
        super().__init__()
        self.is_dead = False
        self.win = False
        self.health = health
        self.total_health = health
        self.win_balls = win_balls
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x, self.y, 70, 80))
        self.speed = 10
        self.vx = 0
        self.vy = 0
        self.gravity = 2
        self.attacking = False
        self.start_attacking = time()
        self.score = 0
        self.manager = manager
        self.game = game

        self.question = Question()
        self.awaiting_answer = False
        self.correct_answer_given = False

        self.question_window = None
        self.answer_entry = None
        self.submit_button = None
        self.feedback_label = None
        self.correct_answer_label = None

        self.animation_frames_right = [load_image(f"pic/hero/hero_walk/hero_walk_{i}.png") for i in range(8)]
        self.animation_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.animation_frames_right]
        self.attack_frames_right = [load_image(f"pic/hero/hero_attack/hero_attack_{i}.png") for i in range(4)]
        self.attack_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.attack_frames_right]
        self.dead_frames = [load_image(f"pic/hero/hero_dead/hero_dead_{i}.png") for i in range(3)]
        self.dead_frame_index = 0
        self.dead_frame_delay = 0.3
        self.last_dead_frame_time = 0
        self.frame_index = 0
        self.image = self.animation_frames_right[self.frame_index]
        self.rect = self.image.get_rect()
        self.direction = "right"

        self.font = pygame.font.Font(None, 36)

    def draw(self, surface, target):
        surface.blit(self.image, self.rect.topleft)

    def draw_dead(self, surface):
        now = time()
        if now - self.last_dead_frame_time > self.dead_frame_delay:
            self.dead_frame_index = (self.dead_frame_index + 1) % len(self.dead_frames)
            self.last_dead_frame_time = now
        surface.blit(self.dead_frames[self.dead_frame_index], self.rect.topleft)

    def update(self):
        if self.rect.left + self.vx < 0:
            self.vx = 0
        if self.rect.right + self.vx > WINDOW_SIZE[0]:
            self.vx = 0

        self.x += self.vx
        self.y += self.vy
        self.rect = pygame.Rect((self.x, self.y, 100, 200))
        self.vx = 0
        self.vy = 0

        now = time()
        if self.attacking and now - self.start_attacking >= 0.5:
            self.attacking = False
            self.image = self.animation_frames_right[self.frame_index] if self.direction == "right" else self.animation_frames_left[self.frame_index]
            self.ask_question()

        if not self.attacking:
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames_right)
            self.image = self.animation_frames_right[self.frame_index] if self.direction == "right" else self.animation_frames_left[self.frame_index]

    def flip_image(self, direction):
        self.direction = direction

    def answer_question(self, answer, target):
        if self.awaiting_answer:
            if self.question.check_answer(answer):
                self.correct_answer_given = True
                self.display_feedback("Ответ верный", (0, 255, 0))
                target.health -= 20
            else:
                self.display_feedback("Ответ неверный", (255, 0, 0))
                self.display_correct_answer(f"Правильный ответ: {self.question.current_question[1]}")
                self.health -= 20
                target.perform_attack(self)
            self.awaiting_answer = False
            self.correct_answer_given = False
            self.remove_question_ui()

    def display_feedback(self, message, color):
        color_hex = '#%02x%02x%02x' % color
        if self.feedback_label:
            self.feedback_label.kill()
        self.feedback_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 200), (400, 50)), 
                                                          text=f'<font color="{color_hex}">{message}</font>', 
                                                          manager=self.manager, container=self.question_window)

    def display_correct_answer(self, message):
        if self.correct_answer_label:
            self.correct_answer_label.kill()
        self.correct_answer_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 250), (400, 50)), 
                                                                text=f'<font color="#ff0000">{message}</font>', 
                                                                manager=self.manager, container=self.question_window)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.l_move()
        if keys[pygame.K_d]:
            self.r_move()
        if keys[pygame.K_SPACE] and not self.awaiting_answer and self.is_near_target(self.game.enemy):
            self.perform_attack(self.game.enemy)

    def l_move(self):
        self.vx = -self.speed
        self.flip_image("left")

    def r_move(self):
        self.vx = self.speed
        self.flip_image("right")

    def is_near_target(self, target):
        return self.rect.colliderect(target.rect.inflate(50, 50))

    def perform_attack(self, target):
        self.attacking = True
        self.start_attacking = time()
        self.r_attack(target)
        pygame.time.set_timer(pygame.USEREVENT, 500)

    def r_attack(self, target):
        if not self.attacking:
            self.attacking = True
            self.start_attacking = time()
            self.image = self.attack_frames_right[0] if self.direction == "right" else self.attack_frames_left[0]
            r_attack_rect = pygame.Rect(self.rect.left - 0.5, self.rect.top - 0.5, self.rect.width + 1, self.rect.height + 1)
            if r_attack_rect.colliderect(target.rect):
                target.health -= 20
            if target.health <= 0:
                self.win = True

    def ask_question(self):
        self.current_question_text = self.question.ask_question()
        if self.current_question_text is None:
            self.game.running = False
            return
        self.awaiting_answer = True
        self.create_question_ui()
        self.game.paused = True

    def create_question_ui(self):
        self.question_window = pygame_gui.elements.UIWindow(rect=pygame.Rect((400, 200), (500, 350)), 
                                                            manager=self.manager, window_display_title="Answer the question",
                                                            object_id=pygame_gui.core.ObjectID(class_id="@question_window"))
        self.question_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 20), (400, 50)), 
                                                          text=self.current_question_text, manager=self.manager, container=self.question_window)
        self.answer_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 80), (400, 30)), 
                                                                manager=self.manager, container=self.question_window)
        self.submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 150), (100, 30)), 
                                                          text='Submit', manager=self.manager, container=self.question_window)

    def remove_question_ui(self):
        if self.question_window:
            self.question_window.kill()
            self.question_window = None
        if self.feedback_label:
            self.feedback_label.kill()
            self.feedback_label = None
        if self.correct_answer_label:
            self.correct_answer_label.kill()
            self.correct_answer_label = None
        self.game.paused = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, health, difficulty):
        super().__init__()
        self.win = False
        self.health = health
        self.total_health = health
        self.is_dead = False  # Добавлен атрибут is_dead
        self.image = None
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x, self.y, 70, 80))
        self.speed = speed
        self.vx = speed
        self.vy = 0
        self.gravity = 2
        self.start_attacking = time()
        self.attacking = False
        self.last_attack_time = time()  # Track last attack time
        self.score = 0
        self.animation_frames_right = [load_image(f"pic/enemy/enemy_walk/enemy_walk_{i}.png") for i in range(8)]
        self.animation_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.animation_frames_right]
        self.attack_frames_right = [load_image(f"pic/enemy/enemy_attack/enemy_attack_{i}.png") for i in range(4)]
        self.attack_frames_left = [pygame.transform.flip(frame, True, False) for frame in self.attack_frames_right]
        self.dead_frames = [load_image(f"pic/enemy/enemy_dead/enemy_dead_{i}.png") for i in range(3)]  # Спрайты мертвого врага
        self.dead_frame_index = 0
        self.dead_frame_delay = 0.3  # Задержка между кадрами анимации смерти
        self.last_dead_frame_time = 0
        self.frame_index = 0
        self.image = self.animation_frames_right[self.frame_index]
        self.rect = self.image.get_rect()
        self.direction = "right"

        self.font = pygame.font.Font(None, 36)
        
        if difficulty == "easy":
            self.damage = 20
            self.attack_cooldown = 90  # 1.5 minutes -> 90 seconds
        elif difficulty == "medium":
            self.damage = 30
            self.attack_cooldown = 60  # 1 minute -> 60 seconds
        elif difficulty == "hard":
            self.damage = 40
            self.attack_cooldown = 45  # 45 seconds

    def draw(self, surface, target):
        surface.blit(self.image, self.rect.topleft)

    def draw_dead(self, surface):
        now = time()
        if now - self.last_dead_frame_time > self.dead_frame_delay:
            self.dead_frame_index = (self.dead_frame_index + 1) % len(self.dead_frames)
            self.last_dead_frame_time = now
        surface.blit(self.dead_frames[self.dead_frame_index], self.rect.topleft)

    def update(self, target):
        if self.rect.left + self.vx < 0 or self.rect.right + self.vx > WINDOW_SIZE[0]:
            self.vx = -self.vx
            self.flip_image()

        if self.rect.x < target.rect.x:
            self.vx = self.speed
            self.direction = "right"
        elif self.rect.x > target.rect.x:
            self.vx = -self.speed
            self.direction = "left"
        else:
            self.vx = 0

        self.x += self.vx
        self.y += self.vy
        self.rect = pygame.Rect((self.x, self.y, 100, 200))

        now = time()
        if self.attacking and now - self.start_attacking >= 0.5:
            self.attacking = False
            self.image = self.animation_frames_right[self.frame_index] if self.direction == "right" else self.animation_frames_left[self.frame_index]

        if not self.attacking:
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames_right)
            self.image = self.animation_frames_right[self.frame_index] if self.direction == "right" else self.animation_frames_left[self.frame_index]
        
        if now - self.last_attack_time >= self.attack_cooldown:
            self.perform_attack(target)
            self.last_attack_time = now

    def flip_image(self):
        self.direction = "left" if self.vx < 0 else "right"

    def is_near_target(self, target):
        return self.rect.colliderect(target.rect.inflate(50, 50))

    def perform_attack(self, target):
        if not self.attacking:
            self.attacking = True
            self.start_attacking = time()
            self.image = self.attack_frames_right[0] if self.direction == "right" else self.attack_frames_left[0]
            attack_rect = pygame.Rect(self.rect.left - 0.5, self.rect.top - 0.5, self.rect.width + 1, self.rect.height + 1)
            if attack_rect.colliderect(target.rect):
                target.health -= self.damage
            if target.health <= 0:
                self.win = True



# Инициализация Pygame и создание окна
pygame.init()
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 700
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
FPS = 60
bg_image = pygame.image.load('pic/bg_game.gif').convert_alpha()

# Создание экземпляра игры и запуск
game = Game(difficulty="easy")  # Set difficulty level here: "easy", "medium", or "hard"
game.run()

pygame.quit()
sys.exit()
