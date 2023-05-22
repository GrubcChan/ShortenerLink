from string import ascii_letters, digits
import sqlite3
import random

class LinkService():
    def __init__(self):
        self.ALPHABET = ascii_letters + digits
        self.LENGTH = 5

    def push(self, url):
        global sqlite_connection
        try:
            sqlite_connection = sqlite3.connect("metanit.db")
            cursor = sqlite_connection.cursor()

            # Проверка, есть ли ссылка в бд
            cursor.execute("SELECT EXISTS(SELECT * FROM urls WHERE link=?)", (url,))
            if not cursor.fetchone()[0]:
                while True:
                    new_hash = self.generate_hash()
                    # Проверка, есть ли хеш в бд
                    cursor.execute("SELECT EXISTS(SELECT * FROM urls WHERE code=?)", (new_hash,))
                    if not cursor.fetchone()[0]:
                        break
                # Добавление новой ссылки в бд
                cursor.execute("INSERT INTO urls (code, link) VALUES (?, ?)", (new_hash, url))
                sqlite_connection.commit()
                return 200, new_hash
            else:
                # Отправка существующего хеша
                cursor.execute("SELECT code FROM urls WHERE link=?", (url,))
                return 200, cursor.fetchone()[0]
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def get(self, hash):
        global sqlite_connection
        try:
            sqlite_connection = sqlite3.connect("metanit.db")
            cursor = sqlite_connection.cursor()

            cursor.execute("SELECT EXISTS(SELECT link FROM urls WHERE code=?)", (hash,))

            if cursor.fetchone()[0]:
                cursor.execute("SELECT link FROM urls WHERE code=?", (hash,))
                return 200, cursor.fetchone()[0]
            else:
                return 404, ''
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def generate_hash(self):
        hash = random.sample(self.ALPHABET, self.LENGTH)
        return ''.join(hash)

