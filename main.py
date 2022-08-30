import telebot
import os
from db import *


bot = telebot.TeleBot('5559031502:AAEYQdWZ3YedTOEn-sHy-5OUjRTgAcHryEE', parse_mode=None)
db = DateBaseUsers('users.db')

list_users = None
index = 0
info = {}
search = {}
user_id_set = None

@bot.message_handler(commands=['start'])
def start(message):
    info['user_id'] = message.chat.id
    photo = open('images/5.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, 'Приветствую. Ты, мой дорогой, попал в самое лучшее место для знакомств'
                                            ' - Badoo')
    msg = bot.send_message(message.chat.id, 'Для начала заполнения анкеты укажите свой номер телефона')
    bot.register_next_step_handler(msg, number)

def start_2(message):
    msg = bot.send_message(message.chat.id, 'Укажите свой номер телефона')
    bot.register_next_step_handler(msg, number)

def number(message):
    number = message.text
    info['number_phone'] = number
    msg = bot.send_message(message.chat.id, 'Введите свою почту')
    bot.register_next_step_handler(msg, email)


def email(message):
    email = message.text
    info['email'] = email
    msg = bot.send_message(message.chat.id, 'Укажите своё полное имя. Пример: Иванов Иван Иванович')
    bot.register_next_step_handler(msg, fio)


def fio(message):
    fio = message.text
    info['fio'] = fio
    msg = bot.send_message(message.chat.id, 'Загрузите своё фото')
    bot.register_next_step_handler(msg, photo)


def photo(message):
    try:
        file_photo = bot.get_file(message.photo[-1].file_id)
        _, file_extension = os.path.splitext(file_photo.file_path)
        downloaded_file = bot.download_file(file_photo.file_path)
        src = 'photos/' + info['fio'] + file_extension
        with open(src, 'wb') as file:
            file.write(downloaded_file)
        info['photo'] = convert_to_binary_data(f'photos/{info["fio"] + file_extension}')
        msg = bot.send_message(message.chat.id, 'Укажите свой возраст')
        bot.register_next_step_handler(msg, user_age)
    except:
        msg = bot.send_message(message.chat.id, 'Это не фото! Пожалуйста, загрузите своё фото')
        bot.register_next_step_handler(msg, photo)


def user_age(message):
    age = message.text
    if not age.isdigit():
        msg = bot.send_message(message.chat.id, 'Пожалуйста, укажите свой возраст в цифрах')
        bot.register_next_step_handler(msg, user_age)
        return
    info['age'] = age
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
            'Комьютер',
            'Программирование',
            'Вязание',
            'Шитьё',
            'Спорт',
    )
    msg = bot.send_message(message.chat.id, 'Ваш основной вид деятельности', reply_markup=markup)
    bot.register_next_step_handler(msg, ovd)


def ovd(message):
    ovd = message.text
    info['ovd'] = ovd
    msg = bot.send_message(message.chat.id, 'Напишите ваши интересы (через запятую)')
    bot.register_next_step_handler(msg, interesty)


def interesty(message):
    interest = message.text
    info['interest'] = interest
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
            'Комунисты',
            'Террористы',
            'Византийцы',
    )
    msg = bot.send_message(message.chat.id, 'Выберите сообщество', reply_markup=markup)
    bot.register_next_step_handler(msg, publish)


def publish(message):
    publish = message.text
    info['publish'] = publish
    msg = bot.send_message(message.chat.id, 'Расскажите немного о себе')
    bot.register_next_step_handler(msg, about_me)


def about_me(message):
    about_me = message.text
    info['about_me'] = about_me
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
        'Найти друга',
        'Найти вторую половинку',
        'Найти людей в команду',
        'Присоединиться к крутому проекту',
    )
    msg = bot.send_message(message.chat.id, 'С какой целью вы посетили наш паблик?', reply_markup=markup)
    bot.register_next_step_handler(msg, logik)

def logik(message):
    params = {
        'Найти друга': 0,
        'Найти вторую половинку': 1,
        'Найти людей в команду': 2,
        'Присоединиться к крутому проекту': 3,
    }
    info['logik'] = params[message.text]
    msg = bot.send_message(message.chat.id, 'Введите свой город')
    bot.register_next_step_handler(msg, sity)


def sity(message):
    city = message.text.lower()
    info['city'] = city
    if not db.user_exists(message.chat.id):
        db.create_new_user(info['user_id'], info['number_phone'], info['email'], info['fio'], info['photo'],
                           info['age'], info['ovd'], info['interest'], info['publish'], info['about_me'], info['logik'], info['city'])
        info.clear()
        msg = bot.send_message(message.chat.id, 'Анкета успешно создана')
        menu(msg)
    else:
        db.change_user(message.chat.id, info['number_phone'], info['email'], info['fio'], info['photo'], info['age'], info['ovd'],
                       info['interest'], info['publish'], info['about_me'], info['logik'], info['city'])
        info.clear()
        msg = bot.send_message(message.chat.id, 'Анкета успешно изменина')
        menu(msg)

@bot.message_handler(commands=['menu'])
def menu(message):
    photo = open('images/8.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
        'Зайти в личный кабинет',
        'Продолжить поиск',
        'Новый поиск',
    )
    msg = bot.send_message(message.chat.id, 'Что будем делать дальше?', reply_markup=markup)
    bot.register_next_step_handler(msg, room)


def room(message):
    global list_users, index
    params = {
        0: 'Восстановить анкету',
        1: 'Остановить анкету'
    }
    if message.text == 'Зайти в личный кабинет':
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(
            'Изменит анкету',
            f'{params[db.get_user_anceta(message.chat.id)]}',
            'Подписка',
        )
        msg = bot.send_message(message.chat.id, 'Что вы хотите узнать?', reply_markup=markup)
        bot.register_next_step_handler(msg, change)

    if message.text == 'Продолжить поиск':
        if not db.search_exists(message.chat.id):
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(
                'Да',
                'Нет',
            )
            msg = bot.send_message(message.chat.id, 'У вас пока что нет предпочтений для поиска. Хотите его создать?', reply_markup=markup)
            bot.register_next_step_handler(msg, create_search)
        else:
            bot.send_message(message.chat.id, 'Начинаю поиск')
            _, logik, publish, city = db.get_search(message.chat.id)[0]
            list_users = db.search(message.chat.id, logik, publish, city)
            if len(list_users) == 0:
                msg = bot.send_message(message.chat.id, 'К сожалению у нас нет пользователей подходящих под ваши интересы')
                bot.register_next_step_handler(msg, room)
            else:
                index = 0
                user_id, number, email, fio, photo, age, ovd, interest, publish, about, city, __, ___, ____ = list_users[index]
                markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.add(
                    'Лайкнуть',
                    'Диз-лайкнуть',
                    'Следующий пост',
                    'Предыдущий пост',
                )
                msg = bot.send_message(message.chat.id,
                                   f'Вот что нам удалось найти:\nФИО - {fio}\nВозраст - {age}\nГород - {city}\n'
                                   f'Основной вид деятельности - {ovd}\nИнтересы - {interest}\n'
                                   f'Сообщество - {publish}\nОбо мне - {about}\nE-mail - {email}\n'
                                   f'Номер телефона - {number}', reply_markup=markup)
                bot.send_photo(message.chat.id, convert_to_binary_data(f"photos/{fio}"))
                bot.register_next_step_handler(msg, user_anketa)

    if message.text == 'Новый поиск':
        msg = bot.send_message(message.chat.id, 'Введите город для поиска')
        bot.register_next_step_handler(msg, search_city)

def create_search(message):
    if message.text == 'Да':
        msg = bot.send_message(message.chat.id, 'Начинаем создавать предпочтения. Введите город для поиска')
        bot.register_next_step_handler(msg, search_city)
    if message.text == 'Нет':
        msg = bot.send_message(message.chat.id, 'Перенапровляю вас в главное меню')
        bot.register_next_step_handler(msg, menu)

def search_city(message):
    search['city'] = message.text.lower()
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
        'Комунисты',
        'Террористы',
        'Византийцы',
    )
    msg = bot.send_message(message.chat.id, 'Выберите сообщество для поиска', reply_markup=markup)
    bot.register_next_step_handler(msg, search_publish)


def search_publish(message):
    search['publish'] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(
        'Найти друга',
        'Найти вторую половинку',
        'Найти людей в команду',
        'Присоединиться к крутому проекту',
    )
    msg = bot.send_message(message.chat.id, 'С какой целью вы ищите? (Выберите из предложеного перечня)', reply_markup=markup)
    bot.register_next_step_handler(msg, search_users)


def search_users(message):
    global list_users, index
    params = {
        'Найти друга': 0,
        'Найти вторую половинку': 1,
        'Найти людей в команду': 2,
        'Присоединиться к крутому проекту': 3,
    }
    search['logik'] = params[message.text]
    if not db.search_exists(message.chat.id):
        db.create_new_search(message.chat.id, search['logik'], search['publish'], search['city'])
        bot.send_message(message.chat.id, 'Данные для поиска успешно сохранены. Начинаю поиск')
        list_users = db.search(message.chat.id, search['logik'], search['publish'], search['city'])
        search.clear()
        if len(list_users) == 0:
            msg = bot.send_message(message.chat.id, 'К сожалению у нас нет пользователей подходящих под ваши интересы')
            bot.register_next_step_handler(msg, room)
        else:
            index = 0
            user_id, number, email, fio, photo, age, ovd, interest, publish, about, city, __, ___, ____ = list_users[index]
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(
                'Лайкнуть',
                'Диз-лайкнуть',
                'Следующий пост',
                'Предыдущий пост',
            )
            msg = bot.send_message(message.chat.id,
                               f'Вот что нам удалось найти:\nФИО - {fio}\nВозраст - {age}\nГород - {city}\n'
                               f'Основной вид деятельности - {ovd}\nИнтересы - {interest}\n'
                               f'Сообщество - {publish}\nОбо мне - {about}\nE-mail - {email}\n'
                               f'Номер телефона - {number}', reply_markup=markup)
            bot.register_next_step_handler(msg, user_anketa)
    else:
        db.change_search(message.chat.id, search['logik'], search['publish'], search['city'])
        bot.send_message(message.chat.id, 'Данные для поиска успешно изменины. Начинаю поиск')
        list_users = db.search(message.chat.id, search['logik'], search['publish'], search['city'])
        search.clear()
        if len(list_users) == 0:
            msg = bot.send_message(message.chat.id, 'К сожалению у нас нет пользователей подходящих под ваши интересы')
            bot.register_next_step_handler(msg, room)
        else:
            index = 0
            user_id, number, email, fio, photo, age, ovd, interest, publish, about, city, __, ___, ____ = list_users[index]
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(
                'Лайкнуть',
                'Диз-лайкнуть',
                'Следующий пост',
                'Предыдущий пост',
            )
            msg = bot.send_message(message.chat.id, f'Вот что нам удалось найти:\nФИО - {fio}\nВозраст - {age}\nГород - {city}\n'
                                          f'Основной вид деятельности - {ovd}\nИнтересы - {interest}\n'
                                          f'Сообщество - {publish}\nОбо мне - {about}\nE-mail - {email}\n'
                                          f'Номер телефона - {number}', reply_markup=markup)
            bot.register_next_step_handler(msg, user_anketa)

def user_anketa(message):
    global list_users, index, user_id_set
    if message.text == "Следующий пост":
        if index == len(list_users)-1:
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(
                'Лайкнуть',
                'Диз-лайкнуть',
                'Следующий пост',
                'Предыдущий пост',
            )
            msg = bot.send_message(message.chat.id, 'Это крайний пользователь списка', reply_markup=markup)
            bot.register_next_step_handler(msg, user_anketa)
        else:
            index += 1
            user_id, number, email, fio, photo, age, ovd, interest, publish, about, city, __, ___, ____ = list_users[index]
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(
                'Лайкнуть',
                'Диз-лайкнуть',
                'Следующий пост',
                'Предыдущий пост',
            )
            msg = bot.send_message(message.chat.id,
                               f'Вот что нам удалось найти:\nФИО - {fio}\nВозраст - {age}\nГород - {city}\n'
                               f'Основной вид деятельности - {ovd}\nИнтересы - {interest}\n'
                               f'Сообщество - {publish}\nОбо мне - {about}\nE-mail - {email}\n'
                               f'Номер телефона - {number}', reply_markup=markup)
            bot.register_next_step_handler(msg, user_anketa)

    if message.text == "Предыдущий пост":
        if index == 0:
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(
                'Лайкнуть',
                'Диз-лайкнуть',
                'Следующий пост',
                'Предыдущий пост',
            )
            msg = bot.send_message(message.chat.id, 'Это крайний пользователь списка', reply_markup=markup)
            bot.register_next_step_handler(msg, user_anketa)
        else:
            index -= 1
            user_id, number, email, fio, photo, age, ovd, interest, publish, about, city, __, ___, ____ = list_users[index]
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(
                'Лайкнуть',
                'Диз-лайкнуть',
                'Следующий пост',
                'Предыдущий пост',
            )
            msg = bot.send_message(message.chat.id,
                               f'Вот что нам удалось найти:\nФИО - {fio}\nВозраст - {age}\nГород - {city}\n'
                               f'Основной вид деятельности - {ovd}\nИнтересы - {interest}\n'
                               f'Сообщество - {publish}\nОбо мне - {about}\nE-mail - {email}\n'
                               f'Номер телефона - {number}', reply_markup=markup)
            bot.register_next_step_handler(msg, user_anketa)

    if message.text == 'Лайкнуть':
        user_id, number, email, fio, photo, age, ovd, interest, publish, about, city, __, ___, ____ = list_users[index]
        bot.send_message(message.chat.id, 'Ваш запрос отправлен')
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(
            'Да',
            'Нет',
            'Посмотреть профиль',
        )
        msg = bot.send_message(user_id, f'Пользователь {db.get_fio(message.chat.id)} поставил вам лайк.'
                                        f'Вы хотите его принять. Если хотите можете cначала посмотреть его профиль',
                               reply_markup=markup)
        user_id_set = message.chat.id
        bot.register_next_step_handler(msg, user_liked)

    if message.text == 'Диз-лайкнуть':
        user_id, number, email, fio, photo, age, ovd, interest, publish, about, city, __, ___, ____ = list_users[index]
        db.set_dis_like(user_id, message.chat.id)
        bot.send_message(message.chat.id, 'Ваши мнение учтено')


def user_liked(message):
    global list_users, index, user_id_set
    if message.text == 'Посмотреть профиль':
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(
            'Да',
            'Нет',
        )
        user_id, number, email, fio, photo, age, ovd, interest, publish, about, city, __, ___, ____ = db.get_user(user_id_set)
        bot.send_message(message.chat.id, f'Вот его профиль:\nФИО - {fio}\nВозраст - {age}\nГород - {city}\n'
                               f'Основной вид деятельности - {ovd}\nИнтересы - {interest}\n'
                               f'Сообщество - {publish}\nОбо мне - {about}\nE-mail - {email}\n'
                               f'Номер телефона - {number}', reply_markup=markup)
        msg = bot.send_message(message.chat.id, 'Теперь вы хотите ответить ему/её взаимностью?')
        bot.register_next_step_handler(msg, set_like)

    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Ваша взаимность отправлена')
        photo = open('images/6.jpg', 'rb')
        bot.send_photo(user_id_set, photo)
        bot.send_message(user_id_set, f'Он/она, {db.get_fio(message.chat.id)}, принял/а ваш лайк!')
        user_id_set = None

    if message.text == 'Нет':
        bot.send_message(message.chat.id, 'Ваша взаимность отправлена')
        photo = open('images/7.jpg', 'rb')
        bot.send_photo(user_id_set, photo)
        bot.send_message(user_id_set, f'К сожалению, он/она, {db.get_fio(message.chat.id)}, откланил/а ваш лайк')
        user_id_set = None

def set_like(message):
    global user_id_set
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Ваша взаимность отправлена')
        photo = open('images/6.jpg', 'rb')
        bot.send_photo(user_id_set, photo)
        bot.send_message(user_id_set, f'Он/она, {db.get_fio(message.chat.id)}, принял/а ваш лайк!')
        user_id_set = None

    if message.text == 'Нет':
        bot.send_message(message.chat.id, 'Ваша взаимность отправлена')
        photo = open('images/7.jpg', 'rb')
        bot.send_photo(user_id_set, photo)
        bot.send_message(user_id_set, f'К сожалению он/она, {db.get_fio(message.chat.id)}, откланил/а ваш лайк')
        user_id_set = None

def change(message):
    if message.text == 'Изменит анкету':
        msg = bot.send_message(message.chat.id, 'Изменение анкеты')
        start_2(msg)
    if message.text == 'Остановить анкету':
        bot.send_message(message.chat.id, 'Анкета остановлена')
        db.stop_user_anceta(message.chat.id)
    if message.text == 'Восстановить анкету':
        bot.send_message(message.chat.id, 'Анкета восстановлена')
        db.start_user_anceta(message.chat.id)
    if message.text == 'Подписка':
        if db.get_subscribe(message.chat.id) == 0:
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(
                'Да',
                'Нет',
            )
            msg = bot.send_message(message.chat.id, 'У вас нет подписки. Желаете ёе приобрести?', reply_markup=markup)
            bot.register_next_step_handler(msg, subscribe)
        if db.get_subscribe(message.chat.id) == 1:
            bot.send_message(message.chat.id, 'У вас есть подписка!', reply_markup=markup)


def subscribe(message):
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Отправьте 5000000 руб и будет вам счастье')
    if message.text == 'Нет':
        bot.send_message(message.chat.id, 'Очень жаль, а ведь вы могли помочь нашему каналу')

bot.infinity_polling()
