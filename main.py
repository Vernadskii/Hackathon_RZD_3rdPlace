""" Функция для запуска """
import telebot
import passwords
bot = telebot.TeleBot(passwords.key)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Реакция на /start"""
    print(message)
    bot.send_message(message.chat.id, "Привет, " + str(message.from_user.first_name)
                 + ", это твой личный друг-аналитик!")
    user_functions.start(message.chat.id, bot)


from functions import user_functions
FUNCTIONS = dict(start=user_functions.start, download_excel=user_functions.download_excel, about_prog=user_functions.about_prog)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Обработик inline-кнопок"""
    try:
        FUNCTIONS[call.data](call.message.chat.id, bot)
    except Exception as ex:
        import logging
        logging.critical(ex)
        logging.critical(" Ошибка в callback_query_handler")


@bot.message_handler(content_types=['document'])
def send_doc(message):
    """ Функция приёма файлов и отправки ссылок на них серверу """

    try:
        bot.send_message(message.chat.id, "Спасибо, я получил первый файл, который буду обрабатывать\n"
                                          "Теперь отправь мне второй...")
        from functions import network_functions
        if network_functions.connect():     # Проверяем, работает ли сервер
            file_url1 = bot.get_file_url(message.document.file_id)
            return bot.register_next_step_handler(message, process_second_file, file_url1)
        else:
            bot.send_message(message.chat.id, "К сожалению, произошла ошибка подключения к серверу :(")
    except Exception as ex:
        import logging
        logging.critical(ex)
        bot.send_message(message.chat.id, "Произошла ошибка обработки файла...")


def process_second_file(message, file_url1):
    file_url2 = bot.get_file_url(message.document.file_id)
    print(file_url1)
    print(file_url2)
    import requests
    r = requests.post('https://urbanml.art/post/excel', files={'file1': file_url1, 'file2': file_url2})
    print(r.text)
    bot.reply_to(message, "Файлы отправлены на вычислительный сервер. Ждём ответа...")


bot.polling(none_stop=False, interval=0, timeout=20)
