import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QPushButton, QMessageBox, QScrollArea, QFrame, QDialog, QComboBox, QFormLayout, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3
from telegram import Bot

class QuestionAnswerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_questions_from_db()

    def initUI(self):
        self.setWindowTitle('Ввод вопросов')
        self.setGeometry(100, 100, 1200, 900)  # Увеличенный размер окна

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)
        
        self.header_label = QLabel('Добавление вопросов и ответов', self)
        self.header_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header_label)
        
        self.question_input = QLineEdit(self)
        self.question_input.setPlaceholderText('Введите вопрос')
        self.question_input.setFont(QFont('Arial', 14))
        self.layout.addWidget(self.question_input)
        
        self.answer_input = QLineEdit(self)
        self.answer_input.setPlaceholderText('Введите ответ')
        self.answer_input.setFont(QFont('Arial', 14))
        self.layout.addWidget(self.answer_input)
        
        self.button_layout = QHBoxLayout()
        
        self.add_button = QPushButton('Добавить вопрос', self)
        self.add_button.setFont(QFont('Arial', 12))
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px; border-radius: 5px;")
        self.add_button.clicked.connect(self.add_question)
        self.button_layout.addWidget(self.add_button)
        
        self.save_button = QPushButton('Сохранить вопросы', self)
        self.save_button.setFont(QFont('Arial', 12))
        self.save_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-size: 14px; border-radius: 5px;")
        self.save_button.clicked.connect(self.save_questions_to_db)
        self.button_layout.addWidget(self.save_button)
        
        self.submit_button = QPushButton('Отправить', self)
        self.submit_button.setFont(QFont('Arial', 12))
        self.submit_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-size: 14px; border-radius: 5px;")
        self.submit_button.clicked.connect(self.open_send_dialog)
        self.button_layout.addWidget(self.submit_button)
        
        self.layout.addLayout(self.button_layout)
        
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        self.question_fields = []
        self.answer_fields = []
        self.questions = []

    def add_question(self):
        question = self.question_input.text()
        answer = self.answer_input.text()
        if question and answer:
            self.questions.append((question, answer))
            self.add_question_answer_field(question, answer)
            self.question_input.clear()
            self.answer_input.clear()

    def add_question_answer_field(self, question='', answer=''):
        question_frame = QFrame()
        question_frame.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;")
        question_layout = QVBoxLayout(question_frame)
        
        question_label = QLabel(f'Вопрос {len(self.question_fields) + 1}:', self)
        question_label.setFont(QFont('Arial', 14))
        question_input = QLineEdit(self)
        question_input.setText(question)
        question_input.setReadOnly(True)
        self.question_fields.append(question_input)
        question_layout.addWidget(question_label)
        question_layout.addWidget(question_input)
        
        answer_label = QLabel('Ответ:', self)
        answer_label.setFont(QFont('Arial', 14))
        answer_input = QLineEdit(self)
        answer_input.setText(answer)
        answer_input.setReadOnly(True)
        self.answer_fields.append(answer_input)
        question_layout.addWidget(answer_label)
        question_layout.addWidget(answer_input)
        
        self.scroll_layout.addWidget(question_frame)

    def load_questions_from_db(self):
        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, answer TEXT)''')
        cursor.execute("SELECT question, answer FROM questions")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.add_question_answer_field(row[0], row[1])

    def save_questions_to_db(self):
        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, answer TEXT)''')
        cursor.executemany("INSERT INTO questions (question, answer) VALUES (?, ?)", self.questions)
        conn.commit()
        conn.close()
        QMessageBox.information(self, 'Сохранение', 'Вопросы успешно сохранены!')

    def open_send_dialog(self):
        dialog = SendDialog(self)
        if dialog.exec_():
            recipient_type = dialog.recipient_type.currentText()
            recipient_name = dialog.recipient_name.currentText()
            self.send_game_to_recipient(recipient_type, recipient_name)

    def send_game_to_recipient(self, recipient_type, recipient_name):
        # Подключение к боту и отправка сообщения
        token = 'YOUR_BOT_TOKEN'
        bot = Bot(token=token)
        chat_id = self.get_chat_id(recipient_type, recipient_name)
        questions_text = self.format_questions()
        link_to_game = "http://yourgame.com/link_to_game"
        message = f"{questions_text}\nСсылка на игру: {link_to_game}"
        bot.send_message(chat_id=chat_id, text=message)
        QMessageBox.information(self, 'Отправка', f'Игра отправлена {recipient_type.lower()} "{recipient_name}"')

    def format_questions(self):
        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT question, answer FROM questions")
        questions = cursor.fetchall()
        response = ""
        for question, answer in questions:
            response += f"Вопрос: {question}\nОтвет: {answer}\n\n"
        conn.close()
        return response

    def get_chat_id(self, recipient_type, recipient_name):
        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (recipient_name,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        return None

    def get_questions_and_answers(self):
        return self.questions

class SendDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Отправка игры')
        self.setGeometry(100, 100, 500, 300)  # Увеличенный размер окна

        self.layout = QVBoxLayout(self)
        
        self.form_layout = QFormLayout()
        
        self.recipient_type = QComboBox(self)
        self.recipient_type.addItems(['Группа', 'Индивидуально'])
        self.recipient_type.setFont(QFont('Arial', 12))
        self.recipient_type.currentTextChanged.connect(self.update_recipient_names)
        self.form_layout.addRow('Тип получателя:', self.recipient_type)
        
        self.recipient_name = QComboBox(self)
        self.recipient_name.setFont(QFont('Arial', 12))
        self.form_layout.addRow('Имя получателя:', self.recipient_name)
        
        self.layout.addLayout(self.form_layout)
        
        self.button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton('ОК', self)
        self.ok_button.setFont(QFont('Arial', 12))
        self.ok_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton('Отмена', self)
        self.cancel_button.setFont(QFont('Arial', 12))
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)
        
        self.layout.addLayout(self.button_layout)
        
        self.update_recipient_names()

    def update_recipient_names(self):
        self.recipient_name.clear()
        conn = sqlite3.connect('student_data.db')
        cursor = conn.cursor()
        if self.recipient_type.currentText() == 'Группа':
            cursor.execute("SELECT DISTINCT group_name FROM users")
            rows = cursor.fetchall()
            groups = [row[0] for row in rows]
            self.recipient_name.addItems(groups)
        else:
            cursor.execute("SELECT username FROM users")
            rows = cursor.fetchall()
            users = [row[0] for row in rows]
            self.recipient_name.addItems(users)
        conn.close()

def main():
    app = QApplication(sys.argv)
    question_app = QuestionAnswerApp()
    question_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
