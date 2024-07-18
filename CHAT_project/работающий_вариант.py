import sys
import codecs
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer, QSize

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BAARSH - Interactive Tutoring")
        self.setGeometry(100, 100, 1280, 900)  # Increased height for window

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

        # Установка центрального виджета и макета
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def set_background_image(self, image_path):
        o_image = QImage(image_path)
        s_image = o_image.scaled(QSize(1280, 900))  # Adjust to your window size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(s_image))
        self.setPalette(palette)

    def create_login_page(self):
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

    def create_training_page(self):
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

    def handle_login(self):
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
        username = self.reg_username_input.text()
        password = self.reg_password_input.text()

        if not username or not password:
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
        quiz_button = QPushButton("Викторина")

        game_button.setObjectName("gameButton")
        quiz_button.setObjectName("gameButton")

        game_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        quiz_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        game_buttons_layout.addWidget(game_button)
        game_buttons_layout.addWidget(quiz_button)

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
        schedule_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(6))
        performance_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(7))
        activity_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(8))

        bottom_buttons_layout.addWidget(assistant_button)
        bottom_buttons_layout.addWidget(schedule_button)
        bottom_buttons_layout.addWidget(performance_button)
        bottom_buttons_layout.addWidget(activity_button)

        layout.addLayout(bottom_buttons_layout)
        home_page.setLayout(layout)
        self.stacked_widget.addWidget(home_page)

    def create_game_page(self):
        game_page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Game Page")
        layout.addWidget(label)
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
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
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
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


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
