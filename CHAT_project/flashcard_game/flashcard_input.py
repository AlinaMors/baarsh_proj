import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QFrame
import requests
class FlashcardInput(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.flashcards = []

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)  # Set window size

        self.layout = QVBoxLayout()

        self.flashcard_list = QListWidget()
        self.layout.addWidget(self.flashcard_list)

        self.input_layout = QVBoxLayout()

        self.question_label = QLabel("Enter Question:")
        self.input_layout.addWidget(self.question_label)

        self.question_input = QTextEdit()
        self.input_layout.addWidget(self.question_input)

        self.answer_label = QLabel("Enter Answer:")
        self.input_layout.addWidget(self.answer_label)

        self.answer_input = QTextEdit()
        self.input_layout.addWidget(self.answer_input)

        self.add_button = QPushButton("Add Flashcard")
        self.add_button.clicked.connect(self.add_flashcard)
        self.input_layout.addWidget(self.add_button)

        self.save_button = QPushButton("Save Flashcards")
        self.save_button.clicked.connect(self.save_flashcards)
        self.input_layout.addWidget(self.save_button)

        self.send_button = QPushButton("Send Flashcards to Telegram")
        self.send_button.clicked.connect(self.send_flashcards_to_telegram)
        self.input_layout.addWidget(self.send_button)

        self.layout.addLayout(self.input_layout)

        self.setLayout(self.layout)
        self.setWindowTitle("Flashcard Input")
        self.apply_styles()
        self.show()

    def add_flashcard(self):
        question = self.question_input.toPlainText()
        answer = self.answer_input.toPlainText()
        if question and answer:
            self.flashcards.append((question, answer))
            self.update_flashcard_list()
            self.question_input.clear()
            self.answer_input.clear()

    def update_flashcard_list(self):
        self.flashcard_list.clear()
        for question, answer in self.flashcards:
            item = QListWidgetItem()
            widget = self.create_flashcard_widget(question, answer)
            item.setSizeHint(widget.sizeHint())
            self.flashcard_list.addItem(item)
            self.flashcard_list.setItemWidget(item, widget)

    def create_flashcard_widget(self, question, answer):
        widget = QWidget()
        layout = QVBoxLayout()

        question_label = QLabel(f"Q: {question}")
        layout.addWidget(question_label)

        answer_label = QLabel(f"A: {answer}")
        layout.addWidget(answer_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        widget.setLayout(layout)
        return widget

    def save_flashcards(self):
        with open("flashcard_game/flashcards.txt", "w") as file:
            for question, answer in self.flashcards:
                file.write(f"{question}\n{answer}\n")
        self.close()  # Close the window after saving

    def send_flashcards_to_telegram(self):
        chat_id = "YOUR_CHAT_ID"
        for question, answer in self.flashcards:
            message = f"Q: {question}\nA: {answer}"
            self.send_to_telegram(chat_id, message)

    def send_to_telegram(self, chat_id, message):
        token = "YOUR_TELEGRAM_BOT_TOKEN"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        response = requests.post(url, data=data)
        return response.json()

    def apply_styles(self):
        with open("flashcard_game/flashcard_style.css", "r") as file:
            self.setStyleSheet(file.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = FlashcardInput()
    sys.exit(app.exec_())
