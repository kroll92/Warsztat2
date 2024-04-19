import hashlib
import psycopg2
from connection import connect_to_db


class User:
    def __init__(self, username, password):
        self.id = -1
        self.username = username
        self._hashed_password = self._hash_password(password)
        self.logged_in = False

    def _hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def login(self, username, password):
        if username == self.username and self._hash_password(password) == self._hashed_password:
            self.logged_in = True
            print("Zalogowano pomyślnie!")
        else:
            print("Błąd logowania: Nieprawidłowa nazwa użytkownika lub hasło.")

    def logout(self):
        self.logged_in = False
        print("Wylogowano.")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def hashed_password(self):
        return self._hashed_password

    @hashed_password.setter
    def hashed_password(self, new_password):
        self._hashed_password = self._hash_password(new_password)
        print("Nowe hasło zostało ustawione.")

    def save_to_db(self):
        try:
            connection = psycopg2.connect(
                dbname="workshop",
                user="postgres",
                password="coderslab",
                host="localhost"
            )
            cursor = connection.cursor()
            if self._id == -1:
                # Nowy użytkownik - zapisz do bazy danych
                cursor.execute("INSERT INTO users (username, hashed_password) VALUES (%s, %s) RETURNING id",
                               (self.username, self.hashed_password))
                self._id = cursor.fetchone()[0]
                print("Użytkownik został dodany do bazy danych.")
            else:
                # Aktualizacja istniejącego użytkownika w bazie danych
                cursor.execute("UPDATE users SET username = %s, hashed_password = %s WHERE id=%s",
                               (self.username, self.hashed_password, self._id))
                print("Użytkownik został zaktualizowany w bazie danych.")
            connection.commit()
            cursor.close()
            connection.close()
        except psycopg2.Error as e:
            print("Wystąpił błąd podczas zapisywania do bazy danych:", e)

    @classmethod
    def load_user_by_username(cls, username):
        try:
            connection = psycopg2.connect(
                dbname="workshop",
                user="postgres",
                password="coderslab",
                host="localhost"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user_data = cursor.fetchone()
            if user_data:
                user = cls(username=user_data[1], password="")
                user._id = user_data[0]
                user._hashed_password = user_data[2]
                return user
            else:
                print("Użytkownik o nazwie {} nie istnieje.".format(username))
                return None
        except psycopg2.Error as e:
            print("Wystąpił błąd podczas wczytywania użytkownika z bazy danych:", e)
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def load_user_by_id(cls, user_id):
        try:
            connection = psycopg2.connect(
                dbname="workshop",
                user="postgres",
                password="coderslab",
                host="localhost"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                user = cls(username=user_data[1], hashed_password="")
                user._id = user_data[0]
                user._hashed_password = user_data[2]
                return user
            else:
                print("Użytkownik o id {id} nie istnieje", format(user_id))
                return None
        except psycopg2.Error as e:
            print("Wystąpił błąd podczas wczytywania użytkownika z bazy danych:", e)
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def load_all_users(cls):
        try:
            connection = psycopg2.connect(
                dbname="workshop",
                user="postgres",
                password="coderslab",
                host="localhost"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            users_data = cursor.fetchall()
            users = []
            for user_data in users_data:
                user = cls(username=users_data[1], password="")
                user._id = users_data[0]
                user._hashed_password = user_data[2]
                users.append(user)
            return users
        except psycopg2.Error as e:
            print("Wystąpił błąd podczas wczytywania użytkowników z bazy danych:", e)
        finally:
            cursor.close()
            connection.close()

    def delete(self):
        try:
            connection = psycopg2.connect(
                dbname="workshop",
                user="postgres",
                password="coderslab",
                host="localhost"
            )
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users WHERE id=%s", (self._id,))
            print("Użytkownik został usunięty z bazy danych.")
            self._id = -1
            connection.commit()
        except psycopg2.Error as e:
            print("Wystąpił błąd podczas usuwania użytkownika z bazy danych:", e)
        finally:
            cursor.close()
            connection.close()


class Message:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None

    @property
    def message_id(self):
        return self._id

    def save_to_db(self):
        try:
            connection = psycopg2.connect(
                dbname="workshop",
                user="postgres",
                password="coderslab",
                host="localhost"
            )
            cursor = connection.cursor()
            if self._id == -1:
                # Nowy użytkownik - zapisz do bazy danych
                cursor.execute("INSERT INTO messages (from_id, to_id, text) VALUES (%s, %s, %s) RETURNING id",
                               (self.from_id, self.to_id, self.text))
                self._id = cursor.fetchone()[0]
                print("Wiadomość została wysłana i dodana do bazy danych.")
            else:
                pass
            connection.commit()
        except psycopg2.Error as e:
            print("Wystąpił błąd podczas zapisywania do bazy danych:", e)
        finally:
            cursor.close()
            connection.close()
