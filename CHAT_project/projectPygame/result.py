import pygame
import sys
import random
import sqlite3

class PicAppear(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

    def update(self, dt):
        pass

class ResultButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, 200)

    def update(self, dt):
        pass

def end():
    pygame.init()
    all_sprites = pygame.sprite.Group()
    car = PicAppear()
    result_button = ResultButton()
    all_sprites.add(car, result_button)

    screen = pygame.display.set_mode((1200, 700))
    pygame.display.set_caption("Game over")

    clock = pygame.time.Clock()
    dt = 0  # Инициализация прошедшего времени
    colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(10)]

    # Создание квадратов
    squares = [pygame.Rect(random.randint(0, 1200-50), random.randint(0, 700-50), 50, 50) for _ in range(10)]
    square_speeds = [(random.randint(1, 5), random.randint(1, 5)) for _ in range(10)]  # Скорость каждого квадрата

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dt = clock.tick(60)  # Получаем прошедшее время с момента последнего вызова
        all_sprites.update(dt)  # Вызываем метод update для всех спрайтов

        # Обработка движения квадратов и проверка на коллизии
        for i in range(10):
            squares[i].move_ip(square_speeds[i])
            if squares[i].left < 0 or squares[i].right > 1200:
                square_speeds[i] = (-square_speeds[i][0], square_speeds[i][1])
            if squares[i].top < 0 or squares[i].bottom > 700:
                square_speeds[i] = (square_speeds[i][0], -square_speeds[i][1])

        screen.fill((0, 0, 0))
        for i in range(10):
            pygame.draw.rect(screen, colors[i], squares[i])
        # Display "вы проиграли" text
        font = pygame.font.Font(None, 74)
        text_surface = font.render("ВЫ ПРОИГРАЛИ", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(600, 350))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

def center_text(text_surface, y, WIDTH, my_window):
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    my_window.blit(text_surface, text_rect)

def information(WIDTH, HEIGHT, my_window):
    current_poloshenie = False
    your_points = pygame.Rect(450, 300, 200, 40)  # Центрирование ввода
    text = ''
    font = pygame.font.Font(None, 36)
    before_color = pygame.Color('#c8ff00')
    after_color = pygame.Color('green')
    color = before_color
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if your_points.collidepoint(event.pos):
                    current_poloshenie = not current_poloshenie
                else:
                    current_poloshenie = False
                color = after_color if current_poloshenie else before_color
            if event.type == pygame.KEYDOWN:
                if current_poloshenie:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        my_window.fill((255, 255, 255))
        a_background_image = pygame.image.load('pic/bg_final_name.jpg')  # Укажите путь к вашему изображению
        a_background_image = pygame.transform.scale(a_background_image, (WIDTH, HEIGHT))
        my_window.blit(a_background_image, (0, 0))
        text_dano = font.render(text, True, color)
        width = max(300, text_dano.get_width() + 10)
        your_points.w = width
        my_window.blit(text_dano, (your_points.x + 5, your_points.y + 5))
        pygame.draw.rect(my_window, color, your_points, 2)

        pygame.display.flip()
        clock.tick(30)

def resultts(balls):
    pygame.init()

    # Размеры окна
    WIDTH, HEIGHT = 1200, 700

    my_window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Registration')

    # Подключение к базе данных SQLite
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Создание таблицы (если ее нет)
    cursor.execute(
        '''CREATE TABLE 
        IF NOT EXISTS example_table
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        score INTEGER)
        ''')

    user_name = information(WIDTH, HEIGHT, my_window)
    user_score = balls

    # Проверка, существует ли уже пользователь с таким именем
    cursor.execute("SELECT * FROM example_table WHERE name=?", (user_name,))
    polzevatel_was_in_db = cursor.fetchone()

    if polzevatel_was_in_db:
        # Если пользователь существует, проверяем, если новый балл выше, обновляем запись
        points = polzevatel_was_in_db[2]
        if user_score > points:
            cursor.execute("UPDATE example_table SET score=? WHERE id=?", (user_score, polzevatel_was_in_db[0]))
    else:
        # Если пользователя с таким именем нет, добавляем новую запись
        cursor.execute("INSERT INTO example_table (name, score) VALUES (?, ?)", (user_name, user_score))

    conn.commit()

    cursor.execute("SELECT * FROM example_table")
    data = cursor.fetchall()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Добавление обоев к слайду с результатами
        background_image = pygame.image.load('pic/bg_results.jpg')  # Укажите путь к вашему изображению
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        my_window.blit(background_image, (0, 0))
        font_a = pygame.font.Font('font/title.ttf', 30)
        # Отрисовка баллов пользователя
        your_score_text = font_a.render(f"Ваш балл: {user_score}", True, ('#f0f095'))
        center_text(your_score_text, 47, WIDTH, my_window)
        center_text(font_a.render(f"Баллы остальных", True, (255, 255, 255)), 98, WIDTH, my_window)
        font_b = pygame.font.Font('font/score.ttf', 20)
        # Отрисовка имени и баллов других пользователей
        y = 180
        for row in data:
            text = f"{row[1]}: {row[2]}"
            rendered_text = font_b.render(text, True, (255, 255, 255))
            center_text(rendered_text, y, WIDTH, my_window)
            y += 50

        pygame.display.flip()

    conn.close()

    pygame.quit()
    sys.exit()
