""" Модуль с сообщениями для пользователей"""
from telebot import types


def start(message_chat_id, bot):
    """Функция приветствия"""
    button1 = types.InlineKeyboardButton(text="📃 О программе", callback_data="about_prog")
    button2 = types.InlineKeyboardButton(text="🧳 Ежедневный отчёт", callback_data="download_excel")
    button3 = types.InlineKeyboardButton(text="🧳 Отчёт за период", callback_data="period")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    bot.send_message(message_chat_id, "Чем тебе помочь?\n", reply_markup=markup)


def download_excel(message_chat_id, bot):
    """Функция, информирующая пользователя об отправке боту excel"""
    button1 = types.InlineKeyboardButton(text="🔙 Назад", callback_data="start")
    types.InlineKeyboardMarkup()
    markup = types.InlineKeyboardMarkup()
    markup.add(button1)
    bot.send_message(message_chat_id, "Просто отправь мне файлы по очереди", reply_markup=markup)


def about_prog(message_chat_id, bot):
    """Функция информирующая пользователя о программе"""
    button1 = types.InlineKeyboardButton(text="🔙 Назад", callback_data="start")
    markup = types.InlineKeyboardMarkup()
    markup.row(button1)
    bot.send_message(message_chat_id, "Я бот-аналитик РЖД\n"
                                      "Я могу составлять отчеты по запросу или по расписанию. "
                                      "Я анализирую работу ремонтых служб и помогаю улучшить работу дороги 🚂",
                     reply_markup=markup)


def do_you_wanna_send_email(message_chat_id, bot):
    """Функция выбора пользователем отправки файла на email"""
    button1 = types.InlineKeyboardButton(text="Хочу 📧️", callback_data="want")
    button2 = types.InlineKeyboardButton(text="Не хочу 📮", callback_data="dont_want")
    markup = types.InlineKeyboardMarkup()
    markup.add(button1, button2)
    bot.send_message(message_chat_id, "Хочешь получить отчёт ещё и на почту?", reply_markup=markup)


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
