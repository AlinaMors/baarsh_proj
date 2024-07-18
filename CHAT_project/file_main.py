import sys
import codecs
import sqlite3
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, QMessageBox, QListWidget, QListWidgetItem, QFrame
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize

from activity_student.user_activity_app import UserActivityApp
from diary_thing.diary import DiaryApp
from projectPygame.questions import QuestionAnswerApp
from victorina.main import QuizApp
from flashcard_game.flashcard_input import FlashcardInput

# Database setup
def create_connection():
    connection = sqlite3.connect('training_user.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    connection.commit()
    return connection

def create_student_db():
    connection = sqlite3.connect('student_data.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE
        )
    ''')
    connection.commit()
    connection.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        print("MainWindow initialization started.")
        self.setWindowTitle("BAARSH - Interactive Tutoring")
        self.setGeometry(100, 100, 1280, 900)  # Increased height for window

        # Регистрация файлов (запускается первой)
        self.register_files()
        create_student_db()  # Create student database

        # Центральный виджет и основной макет
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)  # Center the main layout

        # Создание QStackedWidget для управления страницами
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Создание страниц
        self.create_login_page()
        self.create_training_page()
        self.create_home_page()
        self.create_game_page()
        self.create_quiz_page()
        self.create_assistant_page()
        self.create_schedule_page()
        self.create_performance_page()
        self.create_activity_page()
        self.create_games_selection_page()
        self.create_student_input_page()

        # Установка центрального виджета и макета
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
        print("MainWindow initialization finished.")

    def register_files(self):
        # Здесь добавьте логику регистрации файлов
        print("Регистрация файлов выполнена.")

    def set_background_image(self, image_path):
        o_image = QImage(image_path)
        s_image = o_image.scaled(QSize(1280, 900))  # Adjust to your window size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(s_image))
        self.setPalette(palette)

    def create_login_page(self):
        print("Creating login page.")
        login_page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Center the layout

        form_container = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)  # Center the form layout

        form_container.setObjectName("login_form")

        title_label = QLabel("BAARSH ID")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title_label)

        username_label = QLabel("Имя пользователя")
        self.username_input = QLineEdit()
        password_label = QLabel("Пароль")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Вход")
        register_button = QPushButton("Регистрация")
        
        login_button.clicked.connect(self.handle_login)
        register_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(login_button)
        form_layout.addWidget(register_button)

        form_container.setLayout(form_layout)
        layout.addWidget(form_container)

        login_page.setLayout(layout)
        self.stacked_widget.addWidget(login_page)

        # Подключение стиля для страницы входа
        with codecs.open("training/regist_styles.css", "r", "utf-8") as f:
            login_page.setStyleSheet(f.read())
        print("Login page created.")

    def create_training_page(self):
        print("Creating training page.")
        training_page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Center the layout

        form_container = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)  # Center the form layout

        form_container.setObjectName("training_form")

        title_label = QLabel("Регистрация")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title_label)

        username_label = QLabel("Имя пользователя")
        self.reg_username_input = QLineEdit()
        self.reg_username_input.setObjectName("reg_username_input")  # For CSS styling
        password_label = QLabel("Пароль")
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setObjectName("reg_password_input")  # For CSS styling
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        register_button = QPushButton("Зарегистрироваться")
        back_to_login_button = QPushButton("Назад к Входу")

        register_button.clicked.connect(self.handle_training)
        back_to_login_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        form_layout.addWidget(username_label)
        form_layout.addWidget(self.reg_username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.reg_password_input)
        form_layout.addWidget(register_button)
        form_layout.addWidget(back_to_login_button)

        form_container.setLayout(form_layout)
        layout.addWidget(form_container)

        training_page.setLayout(layout)
        self.stacked_widget.addWidget(training_page)

        # Подключение стиля для страницы регистрации
        with codecs.open("training/regist_styles.css", "r", "utf-8") as f:
            training_page.setStyleSheet(f.read())
        print("Training page created.")

    def handle_login(self):
        print("Handling login.")
        username = self.username_input.text()
        password = self.password_input.text()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            QMessageBox.information(self, "Успешно", "Добро пожаловать!")
            self.stacked_widget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, "Ошибка", "Неправильное имя пользователя или пароль")

    def handle_training(self):
        print("Handling training.")
        username = self.reg_username_input.text()
        password = self.reg_password_input.text()

        if not username or password:
            QMessageBox.warning(self, "Ошибка", "Имя пользователя и пароль не могут быть пустыми")
            return

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            QMessageBox.information(self, "Успешно", "Регистрация завершена!")
            self.stacked_widget.setCurrentIndex(0)
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Имя пользователя уже существует")
        finally:
            conn.close()

    def create_home_page(self):
        print("Creating home page.")
        home_page = QWidget()
        layout = QVBoxLayout()

        self.set_background_image('training/2.png')
        # Подключение стиля для главной страницы
        with codecs.open("training/styles.css", "r", "utf-8") as f:
            home_page.setStyleSheet(f.read())

        # Слайд-шоу
        self.slide_images = [
            "training/slide1.png",
            "training/slide2.png",
            "training/slide3.png",
            "training/slide4.png"
        ]
        self.current_slide = 0

        self.slide_label = QLabel()
        self.slide_label.setPixmap(QPixmap(self.slide_images[self.current_slide]))
        self.slide_label.setScaledContents(True)
        self.slide_label.setFixedSize(1200, 400)

        # Таймер для смены слайдов
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_slide)
        self.timer.start(3000)

        # Индикаторы слайдов
        indicators_layout = QHBoxLayout()
        indicators_layout.setAlignment(Qt.AlignCenter)
        self.indicators = [QLabel("●") for _ in self.slide_images]
        for indicator in self.indicators:
            indicator.setObjectName("indicator")
            indicators_layout.addWidget(indicator)
        self.update_indicators()

        layout.addWidget(self.slide_label)
        layout.addLayout(indicators_layout)

        # Кнопки внизу слайд-шоу
        game_buttons_layout = QHBoxLayout()
        game_button = QPushButton("Начать игру")
        students_button = QPushButton("Мои ученики")

        game_button.setObjectName("gameButton")
        students_button.setObjectName("studentsButton")

        game_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(9))
        students_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(11))

        game_buttons_layout.addWidget(game_button)
        game_buttons_layout.addWidget(students_button)

        layout.addLayout(game_buttons_layout)

        # Кнопки внизу
        bottom_buttons_layout = QHBoxLayout()
        assistant_button = QPushButton("Бот-помощник")
        schedule_button = QPushButton("Расписание")
        performance_button = QPushButton("Успеваемость")
        activity_button = QPushButton("Активность")

        assistant_button.setObjectName("bottomButton")
        schedule_button.setObjectName("bottomButton")
        performance_button.setObjectName("bottomButton")
        activity_button.setObjectName("bottomButton")

        assistant_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))
        schedule_button.clicked.connect(self.open_schedule_window)
        performance_button.clicked.connect(self.open_performance_window)
        activity_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(8))

        bottom_buttons_layout.addWidget(assistant_button)
        bottom_buttons_layout.addWidget(schedule_button)
        bottom_buttons_layout.addWidget(performance_button)
        bottom_buttons_layout.addWidget(activity_button)

        layout.addLayout(bottom_buttons_layout)
        home_page.setLayout(layout)
        self.stacked_widget.addWidget(home_page)

    def open_schedule_window(self):
        self.schedule_window = UserActivityApp()
        self.schedule_window.show()

    def open_performance_window(self):
        self.performance_window = DiaryApp()
        self.performance_window.show()

    def create_game_page(self):
        game_page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Game Page")
        layout.addWidget(label)
        back_button = QPushButton("Back to Game Selection")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(9))
        layout.addWidget(back_button)
        game_page.setLayout(layout)
        self.stacked_widget.addWidget(game_page)

        # Подключение стиля для страницы игры
        with codecs.open("training/styles.css", "r", "utf-8") as f:
            game_page.setStyleSheet(f.read())

    def create_quiz_page(self):
        quiz_page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Quiz Page")
        layout.addWidget(label)
        back_button = QPushButton("Back to Game Selection")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(9))
        layout.addWidget(back_button)
        quiz_page.setLayout(layout)
        self.stacked_widget.addWidget(quiz_page)

        # Подключение стиля для страницы викторины
        with codecs.open("training/styles.css", "r", "utf-8") as f:
            quiz_page.setStyleSheet(f.read())

    def create_assistant_page(self):
        assistant_page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Assistant Page")
        layout.addWidget(label)
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(back_button)
        assistant_page.setLayout(layout)
        self.stacked_widget.addWidget(assistant_page)

        # Подключение стиля для страницы ассистента
        with codecs.open("training/styles.css", "r", "utf-8") as f:
            assistant_page.setStyleSheet(f.read())

    def create_schedule_page(self):
        schedule_page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Schedule Page")
        layout.addWidget(label)
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(back_button)
        schedule_page.setLayout(layout)
        self.stacked_widget.addWidget(schedule_page)

        # Подключение стиля для страницы расписания
        with codecs.open("training/styles.css", "r", "utf-8") as f:
            schedule_page.setStyleSheet(f.read())

    def create_performance_page(self):
        performance_page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Performance Page")
        layout.addWidget(label)
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(back_button)
        performance_page.setLayout(layout)
        self.stacked_widget.addWidget(performance_page)

        # Подключение стиля для страницы успеваемости
        with codecs.open("training/styles.css", "r", "utf-8") as f:
            performance_page.setStyleSheet(f.read())

    def create_activity_page(self):
        activity_page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Activity Page")
        layout.addWidget(label)
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(back_button)
        activity_page.setLayout(layout)
        self.stacked_widget.addWidget(activity_page)

        # Подключение стиля для страницы активности
        with codecs.open("training/styles.css", "r", "utf-8") as f:
            activity_page.setStyleSheet(f.read())

    def create_games_selection_page(self):
        games_selection_page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("Выберите игру")
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; text-align: center; margin-bottom: 20px; background-color: #d3d3d3; padding: 10px;")
        layout.addWidget(title_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)

        fight_button = QPushButton("Бой")
        cards_button = QPushButton("Карточки")
        quiz_button = QPushButton("Квиз")

        fight_button.setObjectName("gameButton")
        cards_button.setObjectName("gameButton")
        quiz_button.setObjectName("gameButton")

        # Adding images to the buttons
        icon_size = QSize(200, 200)
        fight_button.setIcon(QIcon("training/fight.png"))
        fight_button.setIconSize(icon_size)
        cards_button.setIcon(QIcon("training/cards.png"))
        cards_button.setIconSize(icon_size)
        quiz_button.setIcon(QIcon("training/quiz.png"))
        quiz_button.setIconSize(icon_size)

        fight_button.setMinimumSize(icon_size)
        fight_button.setMaximumSize(icon_size)
        cards_button.setMinimumSize(icon_size)
        cards_button.setMaximumSize(icon_size)
        quiz_button.setMinimumSize(icon_size)
        quiz_button.setMaximumSize(icon_size)

        fight_button.clicked.connect(self.open_fight_game)
        cards_button.clicked.connect(self.open_flashcard_input)
        quiz_button.clicked.connect(self.open_quiz_game)

        buttons_layout.addWidget(fight_button)
        buttons_layout.addWidget(cards_button)
        buttons_layout.addWidget(quiz_button)

        layout.addLayout(buttons_layout)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(back_button)

        games_selection_page.setLayout(layout)
        self.stacked_widget.addWidget(games_selection_page)

        # Подключение стиля для страницы выбора игр
        with codecs.open("training/styles.css", "r", "utf-8") as f:
            games_selection_page.setStyleSheet(f.read())

    def create_student_input_page(self):
        student_input_page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("Мои ученики")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()

        name_label = QLabel("Имя ученика")
        self.name_input = QLineEdit()
        phone_label = QLabel("Номер телефона")
        self.phone_input = QLineEdit()
        add_button = QPushButton("Добавить ученика")

        add_button.clicked.connect(self.add_student)

        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(phone_label)
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(add_button)

        layout.addLayout(form_layout)

        # Список учеников
        self.student_list = QListWidget()
        layout.addWidget(self.student_list)
        self.update_student_list()

        student_input_page.setLayout(layout)
        self.stacked_widget.addWidget(student_input_page)

    def add_student(self):
        name = self.name_input.text()
        phone = self.phone_input.text()

        if not name or not phone:
            QMessageBox.warning(self, "Ошибка", "Имя ученика и номер телефона не могут быть пустыми")
            return

        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO students (name, phone) VALUES (?, ?)", (name, phone))
            conn.commit()
            QMessageBox.information(self, "Успешно", "Ученик добавлен!")
            self.name_input.clear()
            self.phone_input.clear()
            self.update_student_list()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Номер телефона уже существует")
        finally:
            conn.close()

    def update_student_list(self):
        self.student_list.clear()
        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone FROM students")
        students = cursor.fetchall()
        conn.close()

        for student in students:
            item = QListWidgetItem(f"{student[0]} - {student[1]}")
            self.student_list.addItem(item)

    def open_fight_game(self):
        self.fight_game_window = QuestionAnswerApp()
        self.fight_game_window.show()

    def open_quiz_game(self):
        self.quiz_game_window = QuizApp()
        self.quiz_game_window.show()

    def open_flashcard_input(self):
        self.flashcard_input_window = FlashcardInput()
        self.flashcard_input_window.show()

    def next_slide(self):
        self.current_slide = (self.current_slide + 1) % len(self.slide_images)
        self.slide_label.setPixmap(QPixmap(self.slide_images[self.current_slide]))
        self.update_indicators()

    def update_indicators(self):
        for i, indicator in enumerate(self.indicators):
            if i == self.current_slide:
                indicator.setStyleSheet("font-size: 36px; color: green;")  # Green color for active slide
            else:
                indicator.setStyleSheet("font-size: 36px; color: gray;")

    def send_to_telegram(self, chat_id, message):
        token = "YOUR_TELEGRAM_BOT_TOKEN"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        response = requests.post(url, data=data)
        return response.json()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
