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
    bot.send_message(message_chat_id, "Выберите месяц:", reply_markup=markup)


def reports(message_chat_id, bot):
    """Функция выбора типа отчётности"""
    button1 = types.InlineKeyboardButton(text="📰 Ежедневный отчёт", callback_data="download_excel")
    button2 = types.InlineKeyboardButton(text="📅 Отчёт за период", callback_data="12345")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1)
    markup.row(button2)
    bot.send_message(message_chat_id, "Выберите тип отчётности:", reply_markup=markup)


def download_excel(message_chat_id, bot):
    """Функция, информирующая пользователя об отправке боту excel"""
    button1 = types.InlineKeyboardButton(text="🔙 Назад", callback_data="start")
    types.InlineKeyboardMarkup()
    markup = types.InlineKeyboardMarkup()
    markup.add(button1)
    bot.send_message(message_chat_id, "Просто отправь мне файлы по очереди (сначала АПВО)", reply_markup=markup)


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
    pass



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
