import sqlite3

def create_tables():
    conn = sqlite3.connect('student_data.db')
    c = conn.cursor()

    # Создание таблицы для групп
    c.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')

    # Создание таблицы для студентов
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            group_id INTEGER,
            FOREIGN KEY(group_id) REFERENCES groups(id)
        )
    ''')

    # Создание таблицы для домашних заданий
    c.execute('''
        CREATE TABLE IF NOT EXISTS homework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            status TEXT,
            description TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')

    # Создание таблицы для платежей
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT,
            amount TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')

    # Создание таблицы для комментариев
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            comment TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')

    # Создание таблицы для присутствия
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT,
            attendance TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_test_data():
    conn = sqlite3.connect('student_data.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM groups")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO groups (name) VALUES ('Группа 1')")
        c.execute("INSERT INTO groups (name) VALUES ('Группа 2')")

        c.execute("INSERT INTO students (name, group_id) VALUES ('Студент 1', 1)")
        c.execute("INSERT INTO students (name, group_id) VALUES ('Студент 2', 1)")
        c.execute("INSERT INTO students (name, group_id) VALUES ('Студент 3', 2)")

        c.execute("INSERT INTO homework (student_id, status, description) VALUES (1, 'Сдано', 'Домашнее задание 1')")
        c.execute("INSERT INTO homework (student_id, status, description) VALUES (1, 'Пропущено', 'Домашнее задание 2')")
        c.execute("INSERT INTO homework (student_id, status, description) VALUES (2, 'Сдано', 'Домашнее задание 3')")
        c.execute("INSERT INTO homework (student_id, status, description) VALUES (3, 'Пропущено', 'Домашнее задание 4')")
        c.execute("INSERT INTO homework (student_id, status, description) VALUES (3, 'Сдано', 'Домашнее задание 5')")

        c.execute("INSERT INTO payments (student_id, date, amount) VALUES (1, '01.01.2024', '1000 руб.')")
        c.execute("INSERT INTO payments (student_id, date, amount) VALUES (1, '01.02.2024', '1000 руб.')")
        c.execute("INSERT INTO payments (student_id, date, amount) VALUES (2, '01.03.2024', '1000 руб.')")

        c.execute("INSERT INTO comments (student_id, comment) VALUES (1, 'Студент активно участвует в занятиях, но иногда пропускает ДЗ.')")

        c.execute("INSERT INTO attendance (student_id, date, attendance) VALUES (1, '01.01.2024', 'Присутствовал')")
        c.execute("INSERT INTO attendance (student_id, date, attendance) VALUES (1, '02.01.2024', 'Отсутствовал')")
        c.execute("INSERT INTO attendance (student_id, date, attendance) VALUES (2, '01.01.2024', 'Присутствовал')")
        c.execute("INSERT INTO attendance (student_id, date, attendance) VALUES (3, '01.01.2024', 'Присутствовал')")
        c.execute("INSERT INTO attendance (student_id, date, attendance) VALUES (3, '02.01.2024', 'Отсутствовал')")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    insert_test_data()
