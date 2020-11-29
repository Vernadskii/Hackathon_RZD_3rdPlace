""" Модуль с сообщениями для пользователей"""
from telebot import types


def start(message_chat_id, bot):
    """Функция приветствия"""
    button1 = types.InlineKeyboardButton(text="📃 О программе", callback_data="about_prog")
    button2 = types.InlineKeyboardButton(text="🧳 Загрузить отчёт", callback_data="reports")
    button3 = types.InlineKeyboardButton(text="🖼️ Визуализировать", callback_data="visualization")
    button4 = types.InlineKeyboardButton(text="💹 Рейтинг", callback_data="rating")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    markup.row(button4)
    bot.send_message(message_chat_id, "Чем вам помочь?\n", reply_markup=markup)


def visualization_series(message_chat_id, bot):
    button1 = types.InlineKeyboardButton(text="ДУОМАТИК09-32GSM", callback_data="DUAMATIK")
    button2 = types.InlineKeyboardButton(text="РПБ-01", callback_data="RPB")
    button3 = types.InlineKeyboardButton(text="ЩОМ-1200М", callback_data="SHOM")
    button4 = types.InlineKeyboardButton(text="ПМГ", callback_data="PMG")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1, button2)
    markup.row(button3, button4)
    bot.send_message(message_chat_id, "Выберите серию:", reply_markup=markup)


def rate_months(message_chat_id, bot):
    button1 = types.InlineKeyboardButton(text="Апрель", callback_data="April")
    button2 = types.InlineKeyboardButton(text="Май", callback_data="May")
    button3 = types.InlineKeyboardButton(text="Июнь", callback_data="June")
    button4 = types.InlineKeyboardButton(text="Июль", callback_data="July")
    button5 = types.InlineKeyboardButton(text="Август", callback_data="August")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1, button2, button3)
    markup.row(button4, button5)
    bot.send_message(message_chat_id, "Выберите месяц 2020-го года:", reply_markup=markup)


def reports(message_chat_id, bot):
    """Функция выбора типа отчётности"""
    download_excel(message_chat_id, bot)


def download_excel(message_chat_id, bot):
    """Функция, информирующая пользователя об отправке боту excel"""
    button1 = types.InlineKeyboardButton(text="🔙 Назад", callback_data="start")
    types.InlineKeyboardMarkup()
    markup = types.InlineKeyboardMarkup()
    markup.add(button1)
    bot.send_message(message_chat_id, "Просто отправьте мне файлы по очереди (сначала АПВО)", reply_markup=markup)


def about_prog(message_chat_id, bot):
    """Функция информирующая пользователя о программе"""
    button1 = types.InlineKeyboardButton(text="🔙 Назад", callback_data="start")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1)
    bot.send_message(message_chat_id, "Я бот-аналитик РЖД\n"
                                      "Я могу составлять отчеты по запросу или по расписанию. "
                                      "Я анализирую работу ремонтых служб и помогаю улучшить работу дороги 🚂",
                     reply_markup=markup)


def rating(message_chat_id, bot):
    button1 = types.InlineKeyboardButton(text="ТОП по остатку", callback_data="top_residue")
    button2 = types.InlineKeyboardButton(text="ТОП по расх. топл. по норме", callback_data="top_rate_norm")
    button3 = types.InlineKeyboardButton(text="ТОП по экономии", callback_data="top_low_rate")
    button4 = types.InlineKeyboardButton(text="ТОП по перерасходу", callback_data="top_up_rate")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    markup.row(button4)
    bot.send_message(message_chat_id, "Выберите категорию:", reply_markup=markup)
    from functions import network_functions
    if network_functions.connect():
        import requests
        #r = requests.get('https://urbanml.art/hello/username')
        columns_map = {
            "date": "Дата работ",
            "machine_type": "Серия машины",
            "value": "Вып. объем физич.",
            "company_y": "Предприятие",
            "au12": "АУ-12",
            "rate_norm": "Расход топлива по норме",
            "rate_fact": "Расход топлива по фактический",
            "low_rate": "Экономия",
            "up_rate": "Перерасход",
            "residue": "Остаток в баках на конец периода"
        }
        """
        {"0": {"machine_type": "\\u0414\\u0423\\u041e\\u041c\\u0410\\u0422\\u0418\\u041a09-32GSM", "machine_number": 39,
               "residue": 103356.0},
         "1": {"machine_type": "\\u041c\\u041f\\u0422-4", "machine_number": 1211, "residue": 29386.0},
         "2": {"machine_type": "\\u041c\\u041f\\u0422-4", "machine_number": 726, "residue": 26308.0},
         "3": {"machine_type": "\\u0414\\u0421\\u041f-\\u04216", "machine_number": 37, "residue": 22936.0},
         "4": {"machine_type": "\\u041c\\u041f\\u0422-4", "machine_number": 381, "residue": 21148.0}}
        """


def month_top(message_chat_id, bot):
    print("month_top")
    button1 = types.InlineKeyboardButton(text="Апрель", callback_data="top_April")
    button2 = types.InlineKeyboardButton(text="Май", callback_data="top_May")
    button3 = types.InlineKeyboardButton(text="Июнь", callback_data="top_June")
    button4 = types.InlineKeyboardButton(text="Июль", callback_data="top_July")
    button5 = types.InlineKeyboardButton(text="Август", callback_data="top_August")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1, button2, button3)
    markup.row(button4, button5)
    bot.send_message(message_chat_id, "Выберите месяц 2020-го года:", reply_markup=markup)


def do_you_wanna_send_email(message_chat_id, bot):
    """Функция выбора пользователем отправки файла на email"""
    button1 = types.InlineKeyboardButton(text="Отправить на email 📧️", callback_data="want")
    button4 = types.InlineKeyboardButton(text="Не хочу 💤", callback_data="start")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1, button4)
    bot.send_message(message_chat_id, "Хочешь получить доп. функцию?", reply_markup=markup)


def want(message_chat_id, bot, src_res):
    """Если пользователь захотел получить письмо на почту"""
    bot.send_message(message_chat_id, "Введи email адрес:")

    @bot.message_handler(content_types=['text'])    # Получаем от пользователя почтовый адрес
    def check_email(message):
        from functions import network_functions
        network_functions.send_email(message.text, src_res, message.chat.first_name)
        button1 = types.InlineKeyboardButton(text="🔙 Начало", callback_data="start")
        markup = types.InlineKeyboardMarkup()
        markup.row(button1)
        bot.send_message(message_chat_id, "Письмо успешно отправлено на " + str(message.text), reply_markup=markup)


def dont_want(message_chat_id, bot):
    """Если пользователь не захотел получить письмо на почту"""
    button1 = types.InlineKeyboardButton(text="🔙 Начало", callback_data="start")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1)
    bot.send_message(message_chat_id, "Хорошо, тогда ты уже можешь заново взаимодействовать со мной нажав кнопку",
                     reply_markup=markup)
