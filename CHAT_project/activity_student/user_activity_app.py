import sys
import sqlite3
import csv
from telegram import Bot
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QProgressBar, QHBoxLayout, QPushButton, 
                             QTextEdit, QMessageBox, QComboBox, QFileDialog, QInputDialog, QTabWidget)
from PyQt5.QtCore import Qt

# Настраиваем Telegram бот
TOKEN = 'YOUR_BOT_TOKEN'
bot = Bot(token=TOKEN)

class UserActivityApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)  # Уменьшаем расстояние между элементами

        # Выбор группы
        group_layout = QHBoxLayout()
        group_label = QLabel("Выберите группу")
        self.group_combobox = QComboBox()
        self.group_combobox.currentIndexChanged.connect(self.load_students)
        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combobox)

        add_group_button = QPushButton("Добавить группу")
        add_group_button.clicked.connect(self.add_group)
        group_layout.addWidget(add_group_button)
        main_layout.addLayout(group_layout)

        # Выбор ученика
        student_layout = QHBoxLayout()
        student_label = QLabel("Выберите ученика")
        self.student_combobox = QComboBox()
        self.student_combobox.currentIndexChanged.connect(self.load_data)
        student_layout.addWidget(student_label)
        student_layout.addWidget(self.student_combobox)

        add_student_button = QPushButton("Добавить ученика")
        add_student_button.clicked.connect(self.add_student)
        student_layout.addWidget(add_student_button)
        main_layout.addLayout(student_layout)

        # Вкладки для отображения данных
        self.tabs = QTabWidget()
        self.homework_tab = QWidget()
        self.payments_tab = QWidget()
        self.attendance_tab = QWidget()
        self.comments_tab = QWidget()

        self.tabs.addTab(self.homework_tab, "Домашние задания")
        self.tabs.addTab(self.payments_tab, "Платежи")
        self.tabs.addTab(self.attendance_tab, "Присутствие")
        self.tabs.addTab(self.comments_tab, "Комментарии")

        self.init_homework_tab()
        self.init_payments_tab()
        self.init_attendance_tab()
        self.init_comments_tab()

        main_layout.addWidget(self.tabs)

        # Прогресс по курсу
        progress_layout = QHBoxLayout()
        progress_label = QLabel("Прогресс по курсу")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(70)  # Пример: 70% завершено
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        main_layout.addLayout(progress_layout)

        # Добавление кнопок управления
        buttons_layout = QHBoxLayout()
        refresh_button = QPushButton("Обновить")
        refresh_button.clicked.connect(self.refresh_data)
        buttons_layout.addWidget(refresh_button)

        export_button = QPushButton("Экспортировать данные")
        export_button.clicked.connect(self.export_data)
        buttons_layout.addWidget(export_button)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Активность пользователя")
        self.setGeometry(100, 100, 1200, 800)  # Увеличиваем ширину окна

        # Применение стилей из файла CSS
        self.setStyleSheet(open("activity_student/activity_style.css").read())

        self.load_groups()
        self.show()

    def init_homework_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)  # Уменьшаем расстояние между элементами

        homework_label = QLabel("Пропущенные/сданные ДЗ")
        layout.addWidget(homework_label)
        self.homework_table = QTableWidget()
        self.homework_table.setColumnCount(2)
        self.homework_table.setHorizontalHeaderLabels(["Статус", "Описание"])
        layout.addWidget(self.homework_table)

        add_homework_button = QPushButton("Добавить ДЗ")
        add_homework_button.clicked.connect(self.add_homework)
        layout.addWidget(add_homework_button)

        self.homework_tab.setLayout(layout)

    def init_payments_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)  # Уменьшаем расстояние между элементами

        payments_label = QLabel("История платежей")
        layout.addWidget(payments_label)
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(2)
        self.payments_table.setHorizontalHeaderLabels(["Дата", "Сумма"])
        layout.addWidget(self.payments_table)

        add_payment_button = QPushButton("Добавить платеж")
        add_payment_button.clicked.connect(self.add_payment)
        layout.addWidget(add_payment_button)

        self.payments_tab.setLayout(layout)

    def init_attendance_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)  # Уменьшаем расстояние между элементами

        attendance_label = QLabel("Присутствие на занятиях")
        layout.addWidget(attendance_label)
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(2)
        self.attendance_table.setHorizontalHeaderLabels(["Дата", "Присутствие"])
        layout.addWidget(self.attendance_table)

        mark_attendance_button = QPushButton("Отметить присутствие")
        mark_attendance_button.clicked.connect(self.mark_attendance)
        layout.addWidget(mark_attendance_button)

        self.attendance_tab.setLayout(layout)

    def init_comments_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)  # Уменьшаем расстояние между элементами

        teacher_comments_label = QLabel("Комментарии преподавателя")
        layout.addWidget(teacher_comments_label)
        self.teacher_comments = QTextEdit()
        layout.addWidget(self.teacher_comments)

        save_comments_button = QPushButton("Сохранить комментарии")
        save_comments_button.clicked.connect(self.save_comments)
        layout.addWidget(save_comments_button)

        self.comments_tab.setLayout(layout)

    def load_groups(self):
        try:
            conn = sqlite3.connect('student_data.db')
            c = conn.cursor()
            c.execute("SELECT id, name FROM groups")
            groups = c.fetchall()
            self.group_combobox.clear()
            self.group_combobox.addItem("Выберите группу", -1)
            for group_id, group_name in groups:
                self.group_combobox.addItem(group_name, group_id)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def load_students(self):
        group_id = self.group_combobox.currentData()
        if group_id == -1:
            return
        try:
            conn = sqlite3.connect('student_data.db')
            c = conn.cursor()
            c.execute("SELECT id, name FROM students WHERE group_id = ?", (group_id,))
            students = c.fetchall()
            self.student_combobox.clear()
            self.student_combobox.addItem("Выберите ученика", -1)
            for student_id, student_name in students:
                self.student_combobox.addItem(student_name, student_id)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def load_data(self):
        student_id = self.student_combobox.currentData()
        if student_id == -1:
            return
        try:
            conn = sqlite3.connect('student_data.db')
            c = conn.cursor()

            # Загрузка данных домашних заданий
            c.execute("SELECT status, description FROM homework WHERE student_id = ?", (student_id,))
            homework_data = c.fetchall()
            self.homework_table.setRowCount(len(homework_data))
            for i, (status, desc) in enumerate(homework_data):
                self.homework_table.setItem(i, 0, QTableWidgetItem(status))
                self.homework_table.setItem(i, 1, QTableWidgetItem(desc))

            # Загрузка данных платежей
            c.execute("SELECT date, amount FROM payments WHERE student_id = ?", (student_id,))
            payments_data = c.fetchall()
            self.payments_table.setRowCount(len(payments_data))
            for i, (date, amount) in enumerate(payments_data):
                self.payments_table.setItem(i, 0, QTableWidgetItem(date))
                self.payments_table.setItem(i, 1, QTableWidgetItem(amount))

            # Загрузка комментариев преподавателя
            c.execute("SELECT comment FROM comments WHERE student_id = ? ORDER BY id DESC LIMIT 1", (student_id,))
            comment = c.fetchone()
            if comment:
                self.teacher_comments.setText(comment[0])
            else:
                self.teacher_comments.clear()

            # Загрузка данных о присутствии
            c.execute("SELECT date, attendance FROM attendance WHERE student_id = ?", (student_id,))
            attendance_data = c.fetchall()
            self.attendance_table.setRowCount(len(attendance_data))
            for i, (date, attendance) in enumerate(attendance_data):
                self.attendance_table.setItem(i, 0, QTableWidgetItem(date))
                self.attendance_table.setItem(i, 1, QTableWidgetItem(attendance))

            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def save_comments(self):
        student_id = self.student_combobox.currentData()
        if student_id == -1:
            return
        try:
            comments = self.teacher_comments.toPlainText()
            conn = sqlite3.connect('student_data.db')
            c = conn.cursor()
            c.execute("INSERT INTO comments (student_id, comment) VALUES (?, ?)", (student_id, comments))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Сохранено", "Комментарии сохранены.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def add_homework(self):
        student_id = self.student_combobox.currentData()
        if student_id == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите ученика для добавления домашнего задания.")
            return

        status, ok = QInputDialog.getText(self, "Статус", "Введите статус домашнего задания:")
        if not ok or not status:
            return

        description, ok = QInputDialog.getText(self, "Описание", "Введите описание домашнего задания:")
        if not ok or not description:
            return

        try:
            conn = sqlite3.connect('student_data.db')
            c = conn.cursor()
            c.execute("INSERT INTO homework (student_id, status, description) VALUES (?, ?, ?)", (student_id, status, description))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Добавлено", "Домашнее задание добавлено.")
            
            # Отправка сообщения через Telegram бот
            self.send_homework_message(student_id, status, description)
            
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def send_homework_message(self, student_id, status, description):
        try:
            conn = sqlite3.connect('bot.db')
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE id = ?", (student_id,))
            user = c.fetchone()
            if user:
                bot.send_message(chat_id=user[0], text=f"Новое домашнее задание: {description} (Статус: {status})")
                QMessageBox.information(self, "Сообщение отправлено", "Сообщение с домашним заданием отправлено.")
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка при отправке сообщения", str(e))

    def add_payment(self):
        student_id = self.student_combobox.currentData()
        if student_id == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите ученика для добавления платежа.")
            return

        date, ok = QInputDialog.getText(self, "Дата", "Введите дату платежа (например, 01.01.2024):")
        if not ok or not date:
            return

        amount, ok = QInputDialog.getText(self, "Сумма", "Введите сумму платежа:")
        if not ok or not amount:
            return

        try:
            conn = sqlite3.connect('student_data.db')
            c = conn.cursor()
            c.execute("INSERT INTO payments (student_id, date, amount) VALUES (?, ?, ?)", (student_id, date, amount))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Добавлено", "Платеж добавлен.")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def mark_attendance(self):
        student_id = self.student_combobox.currentData()
        if student_id == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите ученика для отметки присутствия.")
            return

        date, ok = QInputDialog.getText(self, "Дата", "Введите дату занятия (например, 01.01.2024):")
        if not ok or not date:
            return

        attendance, ok = QInputDialog.getText(self, "Присутствие", "Введите статус присутствия (например, Присутствовал/Отсутствовал):")
        if not ok or not attendance:
            return

        try:
            conn = sqlite3.connect('student_data.db')
            c = conn.cursor()
            c.execute("INSERT INTO attendance (student_id, date, attendance) VALUES (?, ?, ?)", (student_id, date, attendance))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Добавлено", "Присутствие отмечено.")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def add_group(self):
        name, ok = QInputDialog.getText(self, "Добавить группу", "Введите название группы:")
        if not ok or not name:
            return

        try:
            conn = sqlite3.connect('student_data.db')
            c = conn.cursor()
            c.execute("INSERT INTO groups (name) VALUES (?)", (name,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Добавлено", "Группа добавлена.")
            self.load_groups()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def add_student(self):
        group_id = self.group_combobox.currentData()
        if group_id == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите группу для добавления ученика.")
            return

        name, ok = QInputDialog.getText(self, "Добавить ученика", "Введите имя ученика:")
        if not ok or not name:
            return

        try:
            conn = sqlite3.connect('student_data.db')
            c = conn.cursor()
            c.execute("INSERT INTO students (name, group_id) VALUES (?, ?)", (name, group_id))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Добавлено", "Ученик добавлен.")
            self.load_students()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def refresh_data(self):
        self.load_groups()
        self.load_students()
        self.load_data()

    def export_data(self):
        student_id = self.student_combobox.currentData()
        if student_id == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите ученика для экспорта данных.")
            return

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить данные", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            try:
                conn = sqlite3.connect('student_data.db')
                c = conn.cursor()

                c.execute("SELECT status, description FROM homework WHERE student_id = ?", (student_id,))
                homework_data = c.fetchall()

                c.execute("SELECT date, amount FROM payments WHERE student_id = ?", (student_id,))
                payments_data = c.fetchall()

                c.execute("SELECT comment FROM comments WHERE student_id = ? ORDER BY id DESC LIMIT 1", (student_id,))
                comment = c.fetchone()

                c.execute("SELECT date, attendance FROM attendance WHERE student_id = ?", (student_id,))
                attendance_data = c.fetchall()

                with open(fileName, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Домашние задания"])
                    writer.writerow(["Статус", "Описание"])
                    for row in homework_data:
                        writer.writerow(row)

                    writer.writerow([])
                    writer.writerow(["История платежей"])
                    writer.writerow(["Дата", "Сумма"])
                    for row in payments_data:
                        writer.writerow(row)

                    writer.writerow([])
                    writer.writerow(["Комментарии преподавателя"])
                    writer.writerow(["Комментарий"])
                    if comment:
                        writer.writerow([comment[0]])

                    writer.writerow([])
                    writer.writerow(["Присутствие на занятиях"])
                    writer.writerow(["Дата", "Присутствие"])
                    for row in attendance_data:
                        writer.writerow(row)

                conn.close()
                QMessageBox.information(self, "Экспортировано", "Данные успешно экспортированы.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UserActivityApp()
    sys.exit(app.exec_())
