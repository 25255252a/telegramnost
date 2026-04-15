import sqlite3
from user import User
from message import Message


def register_user():
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")

    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, password))
        conn.commit()
        print(f"Пользователь {username} успешно зарегистрирован!")
        return User(username, password, cursor.lastrowid)
    except sqlite3.IntegrityError:
        print("Ошибка: Пользователь с таким именем уже существует!")
        return None
    finally:
        conn.close()


def login():
    username = input("Имя пользователя: ")
    password = input("Пароль: ")

    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                   (username, password))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        print(f"Добро пожаловать, {username}!")
        return User(user_data[1], user_data[2], user_data[0])
    else:
        print("Неверные учётные данные!")
        return None


def send_message(user):
    content = input("Введите сообщение: ")

    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (user_id, content) VALUES (?, ?)",
                   (user.id, content))
    conn.commit()
    conn.close()
    print("Сообщение отправлено!")


def view_messages():
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.username, m.content, m.timestamp
        FROM messages m
        JOIN users u ON m.user_id = u.id
        ORDER BY m.timestamp DESC
        LIMIT 20
    ''')
    messages = cursor.fetchall()
    conn.close()

    print("\n--- Последние сообщения ---")
    for username, content, timestamp in messages:
        print(f"[{timestamp}] {username}: {content}")
    print("------------------------\n")


def main():
    current_user = None

    while True:
        if not current_user:
            print("\n1. Регистрация")
            print("2. Вход")
            choice = input("Выберите действие (1-2): ")

            if choice == "1":
                current_user = register_user()
            elif choice == "2":
                current_user = login()
        else:
            print(f"\n{current_user.username} - Меню:")
            print("1. Отправить сообщение")
            print("2. Просмотреть сообщения")
            print("3. Выйти")
            choice = input("Выберите действие (1-3): ")

            if choice == "1":
                send_message(current_user)
            elif choice == "2":
                view_messages()
            elif choice == "3":
                current_user = None
                print("Вы вышли из системы.")


if __name__ == "__main__":
    main()
