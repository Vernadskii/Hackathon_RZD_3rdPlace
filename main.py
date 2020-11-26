import telebot
import passwords
bot = telebot.TeleBot(passwords.key)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Реакция на /start"""
    print(message)
    bot.send_message(message.chat.id, "Привет, " + str(message.from_user.first_name)
                 + ", это твой личный аналитик-друг!")
    user_functions.start(message.chat.id, bot)


from functions import user_functions

FUNCTIONS = dict(start=user_functions.start, download_excel=user_functions.download_excel, about_prog=user_functions.about_prog)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Обработик inline-кнопок"""
    try:
        #if type(FUNCTIONS[call.data]) is tuple:  # Если у функции есть доп параметр: например имя офиса
        #   print("Вызывается функция с доп параметром")
        #   FUNCTIONS[call.data][0](FUNCTIONS[call.data][1], call, bot)
        #else:  # Если у функции нет доп параметра
        FUNCTIONS[call.data](call.message.chat.id, bot)
    except Exception as ex:
        import logging
        logging.critical(ex)
        logging.critical(" Ошибка в callback_query_handler")


@bot.message_handler(content_types=['document'])
def send_doc(message):
    bot.send_message(message.chat.id, "Спасибо, я получил файл, который буду обрабатывать\n"
                                      "Как только я закончу работу, пришлю тебе ответное письмо...")
    """URL_FOR_FILE = 'https://urbanml.art/post/file'
    import requests
    r = requests.post(URL_FOR_FILE, files=message.document)
    bot.send_message(204181538, message.document.json)
    print(r.text)

    file_id = message.document.file_id
    bot.send_document(message.chat.id, file_id)
    """
    file_url = bot.get_file_url(message.document.file_id)
    print(file_url)

    """
    with open('Отчёт.xlsx', 'rb') as f:
        button1 = types.InlineKeyboardButton(text="🏠 Начало", callback_data="start")
        types.InlineKeyboardMarkup()
        markup = types.InlineKeyboardMarkup()
        markup.add(button1)
        bot.send_document(message.chat.id, f, reply_markup=markup)
    """


bot.polling(none_stop=False, interval=0, timeout=20)
