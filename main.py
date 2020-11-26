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
    bot.send_message(message.chat.id, "Спасибо, я получил файл, который буду обрабатывать\n"
                                      "Как только я закончу работу, пришлю тебе ответное письмо...")
    from functions import network_functions
    if network_functions.connect():
        file = bot.download_file(bot.get_file(message.document.file_id).file_path)  # Получаем объект класса 'bytes'
        src = str(bot.get_file(message.document.file_id).file_path)     # Создали адрес, куда будем сохранять файл
        with open(src, 'wb') as new_file:   # Создали и записали файл
            new_file.write(file)
        with open(src, 'rb') as file_to_send:   # Открываем файл для отправки
            import requests
            r = requests.post('https://urbanml.art/post/excel', files={'file': file_to_send})   # Отправляем файл
            print("Файл успешно отправлен на сервер")
            src = "text files/" + str(bot.get_file(message.document.file_id).file_path)     # Адрес для файла полученного в ответ
            with open(src, 'wb') as new_file:   # Записываем полученный ответ на post
                new_file.write(r.content)
            print("Ответный файл успешно получен")
    else:
        bot.send_message(message.chat.id, "К сожалению, произошла ошибка подключения к серверу :(")

    # file_id = message.document.file_id
    # bot.send_document(message.chat.id, file_id)
    # file_url = bot.get_file_url(message.document.file_id)  # Ссылка на файл, отправленный пользователем
    # bot.get_file(message.document.file_id).file_path     # Получаем адрес файла на сервере
    # в виде "documents/file_6.xlsx"


bot.polling(none_stop=False, interval=0, timeout=20)
