from PyQt5 import QtWidgets, uic
import sys
import sqlite3

class QuizApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(QuizApp, self).__init__()
        uic.loadUi('victorina/quiz.ui', self)  # Загрузка интерфейса из файла quiz.ui
        
        # Подключение сигналов к слотам
        self.add_question_button.clicked.connect(self.add_question)
        self.save_quiz_button.clicked.connect(self.save_quiz)

        self.questions = []

    def add_question(self):
        question_text = self.question_text.text()
        options = [
            self.option1.text(),
            self.option2.text(),
            self.option3.text(),
            self.option4.text()
        ]
        correct_option = self.correct_option.currentText()
        explanation = self.explanation.toPlainText()

        question = {
            "question": question_text,
            "options": options,
            "correct": correct_option,
            "explanation": explanation
        }

        self.questions.append(question)
        self.question_list.addItem(question_text)
        
        # Очистка полей ввода
        self.question_text.clear()
        self.option1.clear()
        self.option2.clear()
        self.option3.clear()
        self.option4.clear()
        self.explanation.clear()

    def save_quiz(self):
        title = self.quiz_title.text()
        difficulty = self.difficulty.currentText()

        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS quizzes
                          (id INTEGER PRIMARY KEY, title TEXT, difficulty TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions
                          (id INTEGER PRIMARY KEY, quiz_id INTEGER, question TEXT, options TEXT, correct TEXT, explanation TEXT)''')

        cursor.execute("INSERT INTO quizzes (title, difficulty) VALUES (?, ?)", (title, difficulty))
        quiz_id = cursor.lastrowid

        for question in self.questions:
            cursor.execute("INSERT INTO questions (quiz_id, question, options, correct, explanation) VALUES (?, ?, ?, ?, ?)",
                           (quiz_id, question['question'], ','.join(question['options']), question['correct'], question['explanation']))

        conn.commit()
        conn.close()

        # Очистка полей ввода и списка вопросов
        self.quiz_title.clear()
        self.questions.clear()
        self.question_list.clear()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()