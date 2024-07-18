import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QStackedWidget, QLabel, QLineEdit, QFormLayout, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import json

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Успеваемость учеников")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.navbar = QHBoxLayout()
        self.layout.addLayout(self.navbar)

        self.student_selector_layout = QHBoxLayout()
        self.layout.addLayout(self.student_selector_layout)

        self.week_button = QPushButton("Успеваемость за неделю")
        self.month_button = QPushButton("Успеваемость за месяц")
        self.semester_button = QPushButton("Успеваемость за полгода")

        self.navbar.addWidget(self.week_button)
        self.navbar.addWidget(self.month_button)
        self.navbar.addWidget(self.semester_button)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.week_page = QWidget()
        self.month_page = QWidget()
        self.semester_page = QWidget()

        self.stacked_widget.addWidget(self.week_page)
        self.stacked_widget.addWidget(self.month_page)
        self.stacked_widget.addWidget(self.semester_page)

        self.week_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.week_page))
        self.month_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.month_page))
        self.semester_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.semester_page))

        self.student_combobox = QComboBox()
        self.student_combobox.setEditable(True)
        self.student_combobox.currentIndexChanged.connect(self.update_data)

        self.student_selector_layout.addWidget(QLabel("Выберите ученика:"))
        self.student_selector_layout.addWidget(self.student_combobox)

        self.students_data = self.load_students_data()
        self.populate_student_combobox()

        self.current_student_data = None

        self.init_pages()

        self.apply_styles()

    def load_students_data(self):
        with open("success_student/student_data.json", "r", encoding="utf-8") as f:
            return json.load(f)["students"]

    def populate_student_combobox(self):
        self.student_combobox.clear()
        for student in self.students_data:
            self.student_combobox.addItem(student["name"])

    def update_data(self):
        student_name = self.student_combobox.currentText()
        self.current_student_data = next((student for student in self.students_data if student["name"] == student_name), None)
        if self.current_student_data:
            self.refresh_pages()

    def load_data(self):
        if self.current_student_data:
            df = pd.DataFrame(self.current_student_data['grades'])
            df['date'] = pd.to_datetime(df['date'])
            return df
        return pd.DataFrame(columns=["date", "score"])

    def init_pages(self):
        self.init_week_page()
        self.init_month_page()
        self.init_semester_page()
        self.refresh_pages()  # Ensure all pages are updated initially

    def init_week_page(self):
        layout = QVBoxLayout()
        self.week_page.setLayout(layout)
        self.week_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.week_canvas)
        self.week_title = QLabel("Успеваемость за неделю")
        layout.addWidget(self.week_title)
        self.add_filter(layout, "week")

    def update_week_page(self):
        if not hasattr(self, 'week_canvas'):
            return
        data = self.load_data()
        if not data.empty:
            data['week'] = data['date'].dt.isocalendar().week
            weekly_data = data.groupby('week')['score'].mean()

            self.week_canvas.axes.clear()
            self.week_canvas.axes.plot(weekly_data, label='Weekly Performance')
            self.week_canvas.axes.set_title('Успеваемость за неделю')
            self.week_canvas.axes.set_xlabel('Неделя')
            self.week_canvas.axes.set_ylabel('Средний балл')
            self.week_canvas.axes.legend()
            self.week_canvas.draw()

            self.update_stats_layout(self.week_page.layout(), weekly_data.mean())

    def init_month_page(self):
        layout = QVBoxLayout()
        self.month_page.setLayout(layout)
        self.month_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.month_canvas)
        self.month_title = QLabel("Успеваемость за месяц")
        layout.addWidget(self.month_title)
        self.add_filter(layout, "month")

    def update_month_page(self):
        if not hasattr(self, 'month_canvas'):
            return
        data = self.load_data()
        if not data.empty:
            data['month'] = data['date'].dt.month
            monthly_data = data.groupby('month')['score'].mean()

            self.month_canvas.axes.clear()
            self.month_canvas.axes.plot(monthly_data, label='Monthly Performance')
            self.month_canvas.axes.set_title('Успеваемость за месяц')
            self.month_canvas.axes.set_xlabel('Месяц')
            self.month_canvas.axes.set_ylabel('Средний балл')
            self.month_canvas.axes.legend()
            self.month_canvas.draw()

            self.update_stats_layout(self.month_page.layout(), monthly_data.mean())

    def init_semester_page(self):
        layout = QVBoxLayout()
        self.semester_page.setLayout(layout)
        self.semester_canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.semester_canvas)
        self.semester_title = QLabel("Успеваемость за полгода")
        layout.addWidget(self.semester_title)
        self.add_filter(layout, "semester")

    def update_semester_page(self):
        if not hasattr(self, 'semester_canvas'):
            return
        data = self.load_data()
        if not data.empty:
            data['semester'] = data['date'].apply(lambda x: (x.month-1)//6 + 1)
            semester_data = data.groupby('semester')['score'].mean()

            self.semester_canvas.axes.clear()
            self.semester_canvas.axes.plot(semester_data, label='Semester Performance')
            self.semester_canvas.axes.set_title('Успеваемость за полгода')
            self.semester_canvas.axes.set_xlabel('Полугодие')
            self.semester_canvas.axes.set_ylabel('Средний балл')
            self.semester_canvas.axes.legend()
            self.semester_canvas.draw()

            self.update_stats_layout(self.semester_page.layout(), semester_data.mean())

    def refresh_pages(self):
        self.update_week_page()
        self.update_month_page()
        self.update_semester_page()

    def add_filter(self, layout, period):
        filter_layout = QFormLayout()
        filter_label = QLabel(f"Фильтр по {period}:")
        self.filter_input = QLineEdit()
        self.filter_button = QPushButton("Применить")
        self.filter_button.clicked.connect(lambda: self.apply_filter(period))
        filter_layout.addRow(filter_label, self.filter_input)
        filter_layout.addWidget(self.filter_button)
        layout.addLayout(filter_layout)

    def apply_filter(self, period):
        try:
            value = int(self.filter_input.text())
            data = self.load_data()
            filtered_data = data[data[period] == value]
            if filtered_data.empty:
                result_text = "Нет данных для выбранного периода"
            else:
                avg_score = filtered_data['score'].mean()
                result_text = f"Средний балл для {period} {value}: {avg_score:.2f}"
        except ValueError:
            result_text = "Некорректный ввод. Пожалуйста, введите числовое значение."

        self.filter_input.setText('')
        self.filter_input.setPlaceholderText(result_text)

    def update_stats_layout(self, layout, mean_value):
        if layout.count() > 2:
            for i in range(2, layout.count()):
                layout.itemAt(i).widget().deleteLater()
        stats_layout = QFormLayout()
        avg_label = QLabel(f"Средний балл: {mean_value:.2f}")
        stats_layout.addRow("Статистика:", avg_label)
        layout.addLayout(stats_layout)

    def apply_styles(self):
        with open("success_student/style_success.css", "r") as f:
            self.setStyleSheet(f.read())

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
