from PyQt5.QtWidgets import QMainWindow, QAction, QCalendarWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QInputDialog, QTimeEdit, QLabel, QTabWidget, QComboBox, QTextEdit, QCheckBox
from PyQt5.QtCore import Qt, QDate, QTime, QTimer, QSize
from PyQt5.QtGui import QColor
import json
import sys
import requests
from PyQt5.QtWidgets import QApplication

class DiaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Ежедневник")
        self.setGeometry(50, 50, 1200, 800)
        
        self.diary_entries = {}
        self.teacher_notifications = False
        
        self.initUI()
    
    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        
        self.tab_widget = QTabWidget(self)
        
        self.daily_tab = QWidget()
        self.weekly_tab = QWidget()
        self.monthly_tab = QWidget()
        
        self.tab_widget.addTab(self.daily_tab, "День")
        self.tab_widget.addTab(self.weekly_tab, "Неделя")
        self.tab_widget.addTab(self.monthly_tab, "Месяц")
        
        self.init_daily_tab()
        self.init_weekly_tab()
        self.init_monthly_tab()
        
        self.layout.addWidget(self.tab_widget)
        self.central_widget.setLayout(self.layout)
        
        self.create_menu()
        self.load_diary()
        self.apply_styles()
        self.highlight_days_with_events()
        self.start_notifications()
    
    def init_daily_tab(self):
        self.daily_layout = QVBoxLayout()
        
        self.calendar = QCalendarWidget(self)
        self.calendar.clicked.connect(self.load_tasks_for_selected_date)
        
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm")
        
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Введите событие")
        
        self.task_description = QTextEdit(self)
        self.task_description.setPlaceholderText("Введите описание события")
        
        self.task_location = QLineEdit(self)
        self.task_location.setPlaceholderText("Введите ссылку для входа на урок")
        
        self.additional_material = QLineEdit(self)
        self.additional_material.setPlaceholderText("Введите ссылку на дополнительный материал (по желанию)")
        
        self.photo_link = QLineEdit(self)
        self.photo_link.setPlaceholderText("Введите ссылку на фотографию (по желанию)")
        
        self.reminder_combo = QComboBox(self)
        self.reminder_combo.addItems(["Нет напоминания", "За 5 минут", "За 10 минут", "За 15 минут", "За 30 минут", "За 1 час"])
        
        self.repeat_combo = QComboBox(self)
        self.repeat_combo.addItems(["Не повторяется", "Ежедневно", "Еженедельно", "Ежемесячно", "Ежегодно"])
        
        self.color_combo = QComboBox(self)
        self.color_combo.addItems(["Без цвета", "Красный", "Зелёный", "Синий", "Жёлтый"])
        
        self.add_task_button = QPushButton("Добавить событие", self)
        self.add_task_button.clicked.connect(self.add_task)
        
        self.tasks_table = QTableWidget(self)
        self.tasks_table.setColumnCount(8)
        self.tasks_table.setHorizontalHeaderLabels(["Время", "Событие", "Ссылка на урок", "Описание", "Напоминание", "Доп. материал", "Фото", "Действия"])
        
        self.daily_layout.addWidget(self.calendar)
        
        task_layout = QVBoxLayout()
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Время:"))
        input_layout.addWidget(self.time_edit)
        input_layout.addWidget(QLabel("Событие:"))
        input_layout.addWidget(self.task_input)
        
        task_layout.addLayout(input_layout)
        task_layout.addWidget(self.task_description)
        task_layout.addWidget(self.task_location)
        task_layout.addWidget(QLabel("Напоминание:"))
        task_layout.addWidget(self.reminder_combo)
        task_layout.addWidget(QLabel("Повторение:"))
        task_layout.addWidget(self.repeat_combo)
        task_layout.addWidget(QLabel("Цвет:"))
        task_layout.addWidget(self.color_combo)
        task_layout.addWidget(self.additional_material)
        task_layout.addWidget(self.photo_link)
        task_layout.addWidget(self.add_task_button)
        
        self.daily_layout.addLayout(task_layout)
        self.daily_layout.addWidget(self.tasks_table)
        
        self.daily_tab.setLayout(self.daily_layout)
    
    def init_weekly_tab(self):
        self.weekly_layout = QVBoxLayout()
        
        self.weekly_table = QTableWidget(self)
        self.weekly_table.setColumnCount(2)
        self.weekly_table.setHorizontalHeaderLabels(["Дата", "События"])
        
        self.weekly_layout.addWidget(self.weekly_table)
        
        self.weekly_tab.setLayout(self.weekly_layout)
    
    def init_monthly_tab(self):
        self.monthly_layout = QVBoxLayout()
        
        self.monthly_calendar = QCalendarWidget(self)
        self.monthly_calendar.setGridVisible(True)
        self.monthly_calendar.clicked.connect(self.load_tasks_for_selected_date)
        
        self.monthly_layout.addWidget(self.monthly_calendar)
        self.monthly_tab.setLayout(self.monthly_layout)
    
    def create_menu(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("Файл")
        
        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_diary)
        
        load_action = QAction("Загрузить", self)
        load_action.triggered.connect(self.load_diary)
        
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
    
    def load_tasks_for_selected_date(self):
        selected_date = self.calendar.selectedDate().toString(Qt.ISODate)
        self.task_input.clear()
        self.tasks_table.setRowCount(0)
        
        if selected_date in self.diary_entries:
            tasks = self.diary_entries[selected_date]
            for task in tasks:
                self.add_task_to_table(task)
        
        self.load_weekly_tasks()
    
    def add_task(self):
        selected_date = self.calendar.selectedDate().toString(Qt.ISODate)
        task_time = self.time_edit.time().toString("HH:mm")
        task_description = self.task_input.text().strip()
        task_full_description = self.task_description.toPlainText().strip()
        task_location = self.task_location.text().strip()
        additional_material = self.additional_material.text().strip()
        photo_link = self.photo_link.text().strip()
        task_reminder = self.reminder_combo.currentText()
        task_repeat = self.repeat_combo.currentText()
        task_color = self.color_combo.currentText()
        
        if not task_description:
            QMessageBox.warning(self, "Ошибка", "Событие не может быть пустым")
            return
        
        task = {
            "time": task_time,
            "description": task_description,
            "full_description": task_full_description,
            "location": task_location,
            "reminder": task_reminder,
            "repeat": task_repeat,
            "color": task_color,
            "additional_material": additional_material,
            "photo_link": photo_link
        }
        
        if selected_date not in self.diary_entries:
            self.diary_entries[selected_date] = []
        
        self.diary_entries[selected_date].append(task)
        self.add_task_to_table(task)
        self.task_input.clear()
        self.task_description.clear()
        self.task_location.clear()
        self.additional_material.clear()
        self.photo_link.clear()
        self.highlight_days_with_events()
        
        self.send_to_telegram_bot(selected_date, task)
    
    def add_task_to_table(self, task):
        row_position = self.tasks_table.rowCount()
        self.tasks_table.insertRow(row_position)
        self.tasks_table.setItem(row_position, 0, QTableWidgetItem(task["time"]))
        self.tasks_table.setItem(row_position, 1, QTableWidgetItem(task["description"]))
        self.tasks_table.setItem(row_position, 2, QTableWidgetItem(task["location"]))
        self.tasks_table.setItem(row_position, 3, QTableWidgetItem(task["full_description"]))
        self.tasks_table.setItem(row_position, 4, QTableWidgetItem(task["reminder"]))
        self.tasks_table.setItem(row_position, 5, QTableWidgetItem(task["additional_material"]))
        self.tasks_table.setItem(row_position, 6, QTableWidgetItem(task["photo_link"]))
        
        edit_button = QPushButton("Редактировать")
        edit_button.setFixedSize(QSize(100, 30))
        edit_button.clicked.connect(lambda: self.edit_task(row_position))
        delete_button = QPushButton("Удалить")
        delete_button.setFixedSize(QSize(100, 30))
        delete_button.clicked.connect(lambda: self.delete_task(row_position))
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        
        self.tasks_table.setCellWidget(row_position, 7, button_widget)
        
        if task["color"] != "Без цвета":
            self.color_task_row(row_position, task["color"])
    
    def color_task_row(self, row, color):
        color_dict = {
            "Красный": QColor("#FFCDD2"),
            "Зелёный": QColor("#C8E6C9"),
            "Синий": QColor("#BBDEFB"),
            "Жёлтый": QColor("#FFF9C4")
        }
        
        for column in range(self.tasks_table.columnCount() - 1):  # Skip the last column with buttons
            item = self.tasks_table.item(row, column)
            if item:
                item.setBackground(color_dict.get(color, QColor(Qt.white)))
    
    def edit_task(self, row):
        selected_date = self.calendar.selectedDate().toString(Qt.ISODate)
        task = self.diary_entries[selected_date][row]
        
        new_time, ok_time = QInputDialog.getText(self, "Редактировать время", "Время (HH:mm):", text=task["time"])
        new_description, ok_desc = QInputDialog.getText(self, "Редактировать событие", "Событие:", text=task["description"])
        
        if ok_time and ok_desc and new_time and new_description:
            task["time"] = new_time
            task["description"] = new_description
            self.tasks_table.setItem(row, 0, QTableWidgetItem(new_time))
            self.tasks_table.setItem(row, 1, QTableWidgetItem(new_description))
    
    def delete_task(self, row):
        selected_date = self.calendar.selectedDate().toString(Qt.ISODate)
        del self.diary_entries[selected_date][row]
        self.tasks_table.removeRow(row)
        self.highlight_days_with_events()
    
    def load_weekly_tasks(self):
        self.weekly_table.setRowCount(0)
        
        current_date = self.calendar.selectedDate()
        start_of_week = current_date.addDays(-current_date.dayOfWeek() + 1)
        
        for i in range(7):
            day = start_of_week.addDays(i)
            date_str = day.toString(Qt.ISODate)
            
            row_position = self.weekly_table.rowCount()
            self.weekly_table.insertRow(row_position)
            self.weekly_table.setItem(row_position, 0, QTableWidgetItem(day.toString("dddd, dd MMMM yyyy")))
            
            if date_str in self.diary_entries:
                tasks = self.diary_entries[date_str]
                task_texts = "\n".join([f"{task['time']} - {task['description']}" for task in tasks])
                self.weekly_table.setItem(row_position, 1, QTableWidgetItem(task_texts))
            else:
                self.weekly_table.setItem(row_position, 1, QTableWidgetItem("Нет событий"))
    
    def highlight_days_with_events(self):
        for date in self.diary_entries.keys():
            date_qdate = QDate.fromString(date, Qt.ISODate)
            if date_qdate:
                format = self.calendar.dateTextFormat(date_qdate)
                format.setBackground(Qt.yellow)
                self.calendar.setDateTextFormat(date_qdate, format)
                self.monthly_calendar.setDateTextFormat(date_qdate, format)
    
    def start_notifications(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_notifications)
        self.timer.start(60000)
    
    def check_for_notifications(self):
        current_date = QDate.currentDate().toString(Qt.ISODate)
        current_time = QTime.currentTime().toString("HH:mm")
        
        if current_date in self.diary_entries:
            for task in self.diary_entries[current_date]:
                if task["time"] == current_time:
                    QMessageBox.information(self, "Напоминание", f"Событие: {task['description']}")
                    if self.teacher_notifications:
                        self.send_to_teacher(task["description"])
    
    def save_diary(self):
        with open('diary.json', 'w') as file:
            json.dump(self.diary_entries, file)
        QMessageBox.information(self, "Сохранено", "Дневник сохранён")
    
    def load_diary(self):
        try:
            with open('diary.json', 'r') as file:
                self.diary_entries = json.load(file)
            self.highlight_days_with_events()
        except FileNotFoundError:
            pass
    
    def apply_styles(self):
        with open("diary_thing/styles.css", "r") as file:
            self.setStyleSheet(file.read())
    
    def toggle_notifications(self, state):
        self.teacher_notifications = bool(state)
    
    def send_to_teacher(self, message):
        # Здесь используйте API для отправки уведомления учителю
        pass
    
    def send_to_telegram_bot(self, date, task):
        token = "YOUR_BOT_TOKEN"
        chat_id = "YOUR_CHAT_ID"
        text = (
            f"Дата: {date}\n"
            f"Время: {task['time']}\n"
            f"Событие: {task['description']}\n"
            f"Описание: {task['full_description']}\n"
            f"Ссылка на урок: {task['location']}\n"
            f"Напоминание: {task['reminder']}\n"
            f"Повторение: {task['repeat']}\n"
            f"Доп. материал: {task['additional_material']}\n"
            f"Фото: {task['photo_link']}"
        )
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)

    def repeat_schedule(self):
        selected_date = self.calendar.selectedDate()
        for month in range(1, 13):
            next_date = QDate(selected_date.year(), month, selected_date.day())
            if next_date not in self.diary_entries:
                self.diary_entries[next_date.toString(Qt.ISODate)] = self.diary_entries[selected_date.toString(Qt.ISODate)]
        self.highlight_days_with_events()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiaryApp()
    window.show()
    sys.exit(app.exec_())
