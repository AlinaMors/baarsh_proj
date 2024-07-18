from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import sqlite3
from datetime import datetime

# Настраиваем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s',
                    level=logging.INFO)

TOKEN = '7267417446:AAHqa4BN6QJBiJkS7S403McL8ap4Lew0XyY'

# Подключаемся к базе данных SQLite
conn = sqlite3.connect('bot.db', check_same_thread=False)
cursor = conn.cursor()

# Создаем таблицы, если они еще не созданы
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS classes (id INTEGER PRIMARY KEY, title TEXT, date_time TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, deadline TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY, user_id INTEGER, reminder_time TEXT, type TEXT)''')
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    cursor.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (user.id, user.username))
    conn.commit()
    await update.message.reply_text('Добро пожаловать! Используйте /help для просмотра доступных команд.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('/addclass - Добавить новое занятие\n/addtask - Добавить новое задание\n/setreminder - Установить напоминание\n/viewclasses - Просмотреть предстоящие занятия\n/viewtasks - Просмотреть задания и тесты')

async def add_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        title = context.args[0]
        date_time = context.args[1]
        cursor.execute("INSERT INTO classes (title, date_time) VALUES (?, ?)", (title, date_time))
        conn.commit()
        await update.message.reply_text('Занятие успешно добавлено!')
    except IndexError:
        await update.message.reply_text('Использование: /addclass <название> <дата_время>')

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        title = context.args[0]
        deadline = context.args[1]
        cursor.execute("INSERT INTO tasks (title, deadline) VALUES (?, ?)", (title, deadline))
        conn.commit()
        await update.message.reply_text('Задание успешно добавлено!')
    except IndexError:
        await update.message.reply_text('Использование: /addtask <название> <дедлайн>')

async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        reminder_time = context.args[0]
        reminder_type = context.args[1]
        user_id = update.message.from_user.id
        cursor.execute("INSERT INTO reminders (user_id, reminder_time, type) VALUES (?, ?, ?)", (user_id, reminder_time, reminder_type))
        conn.commit()
        await update.message.reply_text('Напоминание успешно установлено!')
    except IndexError:
        await update.message.reply_text('Использование: /setreminder <время_напоминания> <тип>')

async def view_classes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cursor.execute("SELECT title, date_time FROM classes")
    classes = cursor.fetchall()
    if classes:
        response = "\n".join([f"{cls[0]} - {cls[1]}" for cls in classes])
    else:
        response = "Предстоящих занятий нет."
    await update.message.reply_text(response)

async def view_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cursor.execute("SELECT title, deadline FROM tasks")
    tasks = cursor.fetchall()
    if tasks:
        response = "\n".join([f"{task[0]} - {task[1]}" for task in tasks])
    else:
        response = "Заданий нет."
    await update.message.reply_text(response)

async def send_notifications(context: CallbackContext) -> None:
    cursor.execute("SELECT user_id, type, reminder_time FROM reminders")
    reminders = cursor.fetchall()
    for reminder in reminders:
        user_id, reminder_type, reminder_time = reminder
        now = datetime.now()
        reminder_dt = datetime.strptime(reminder_time, '%Y-%m-%d %H:%М:%S')
        if now >= reminder_dt:
            await context.bot.send_message(chat_id=user_id, text=f"Напоминание: {reminder_type}")
            cursor.execute("DELETE FROM reminders WHERE user_id = ? AND reminder_time = ? AND type = ?", (user_id, reminder_time, reminder_type))
            conn.commit()

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addclass", add_class))
    application.add_handler(CommandHandler("addtask", add_task))
    application.add_handler(CommandHandler("setreminder", set_reminder))
    application.add_handler(CommandHandler("viewclasses", view_classes))
    application.add_handler(CommandHandler("viewtasks", view_tasks))

    scheduler = BackgroundScheduler()
    scheduler.add_job(send_notifications, 'interval', minutes=1, args=(application.bot,))
    scheduler.start()

    application.run_polling()

if __name__ == '__main__':
    main()
