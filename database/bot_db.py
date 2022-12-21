import random
import sqlite3
from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect('bot.sqlite3')
    cursor = db.cursor()

    if db:
        print("База данных подключена")

    db.execute(
        "CREATE TABLE IF NOT EXISTS mentors"
        "(id INTEGER PRIMARY KEY, name TEXT,"
        " nap TEXT, age INTEGER, grup TEXT)"
    )

    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO mentors VALUES (?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM mentors").fetchall()
    random_mentor = random.choice(result)
    await bot.send_message(message.from_user.id,
                           f"id - {random_mentor[0]}, name - {random_mentor[1]}, nap - {random_mentor[2]},"
                           f"age - {random_mentor[3]}, grup - {random_mentor[4]}")


async def sql_command_all():
    return cursor.execute('SELECT * FROM mentors').fetchall()


async def sql_command_delete(mentor_id):
    cursor.execute("DELETE FROM mentors WHERE id = ?", (mentor_id,))
    db.commit()