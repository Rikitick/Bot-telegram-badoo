import sqlite3

class DateBaseUsers:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()


    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id, )).fetchmany(1)
            return bool(len(result))


    def get_fio(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT fio FROM users WHERE user_id = ?", (user_id, )).fetchmany(1)[0][0]

    def get_all_user(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users")
            return result

    def create_new_user(self, user_id, number_phone, email, fio, photo, age, ovd, interest, publish, about_me, logik, city):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, publish, about, number, city, email,"
                                       " fio, photo, age, ovd, interest, logik) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                       (user_id, publish, about_me, number_phone, city.lower(), email, fio, photo, age, ovd, interest, logik, ))

    def change_user(self, user_id, number_phone, email, fio, photo, age, ovd, interest, publish, about_me, logik, city):
        with self.connection:
            return self.cursor.execute("UPDATE users SET publish = ?, about = ?, number = ?, city = ?,"
                                       " email = ?, fio = ?, photo = ?,"
                                       f" age = ?, ovd = ?, interest = ?, logik = ? WHERE user_id = {user_id}",
                                       (publish, about_me, number_phone, city.lower(), email, fio, photo, age, ovd, interest, logik, ))

    def get_user_anceta(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT active FROM users WHERE user_id = ?", (user_id, )).fetchmany(1)
            return result[0][0]


    def stop_user_anceta(self, user_id):
        with self.connection:
            return self.cursor.execute('UPDATE users SET active = 0 WHERE user_id = ?', (user_id, ))

    def start_user_anceta(self, user_id):
        with self.connection:
            return self.cursor.execute('UPDATE users SET active = 1 WHERE user_id = ?', (user_id, ))

    def get_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id, )).fetchmany(1)
            return result[0]

    def get_subscribe(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT subscribe FROM users WHERE user_id = ?", (user_id, )).fetchmany(1)
            return result[0][0]

    def get_search(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM search WHERE user_id = ?", (user_id, )).fetchmany(1)
            return result

    def create_new_search(self, user_id, logik, publish, city):
        with self.connection:
            return self.cursor.execute("INSERT INTO search (user_id, logik, publish, city) VALUES (?, ?, ?, ?)",
                                       (user_id, logik, publish, city.lower(), ))

    def change_search(self, user_id, logik,  publish, city):
        with self.connection:
            return self.cursor.execute(f"UPDATE search SET publish = ?, logik = ?, city = ? WHERE user_id = {user_id}",
                                       (publish, logik, city.lower(), ))

    def search_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM search WHERE user_id = ?", (user_id, )).fetchmany(1)
            return bool(len(result))

    def search(self, user_id, logik, publish, city):
        with self.connection:
            if logik == 2:
                index = 0
                list = self.cursor.execute("SELECT * FROM users WHERE user_id != ? AND logik = 3 AND publish = ? "
                                                 "AND city = ?", (user_id, publish, city.lower(), )).fetchall()
                for i in list:
                    user_id_liked, number, email, fio, photo, age, ovd, interest, publish, about, city, __, ___, ____ = i
                    if self.get_like(user_id_liked) == 0 or self.get_like(user_id) is None:
                        list.pop(index)
                        index += 1

                return list
            if logik == 3:
                index = 0
                list = self.cursor.execute("SELECT * FROM users WHERE user_id != ? AND logik = 2 AND publish = ? "
                                                 "AND city = ?", (user_id, publish, city.lower(), )).fetchall()
                for i in list:
                    user_id_liked, number, email, fio, photo, age, ovd, interest, publish, about, city, __, ___, ____ = i
                    if self.get_like(user_id_liked) == 0 or self.get_like(user_id) is None:
                        list.pop(index)
                        index += 1

                return list
            else:
                index = 0
                list = self.cursor.execute("SELECT * FROM users WHERE user_id != ? AND logik = ? AND publish = ? "
                                                 "AND city = ?", (user_id, logik, publish, city.lower(), )).fetchall()
                for i in list:
                    user_id_liked, number, email, fio, photo, age, ovd, interest, publish, about, city, __, ___, ____ = i
                    try:
                        if self.get_like(user_id_liked) == 0:
                            list.pop(index)
                            index += 1
                    except:
                        break

                return list

    def get_like(self, user_id_liked):
        with self.connection:
            result = self.cursor.execute("SELECT emoji FROM likes WHERE user_id_liked = ?", (user_id_liked, )).fetchmany(1)
            return result[0][0]

    def set_dis_like(self, user_id_liked, user_id_set):
        with self.connection:
            self.cursor.execute('INSERT INTO likes (user_id_liked, user_id_set, emoji) VALUES (?, ?, ?)', (user_id_liked, user_id_set, 0))


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

