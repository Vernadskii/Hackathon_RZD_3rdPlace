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
    """ Не очень оптимизированная функция обработки файла.
        Функция отправляет полученный файл от пользователя и отправляет его на сервер,
        далее получает обработанный и отправляет его конечному пользователю"""
    import os
    try:
        bot.send_message(message.chat.id, "Спасибо, я получил файл, который буду обрабатывать\n"
                                          "Как только я закончу работу, пришлю тебе обработанный файл...")
        from functions import network_functions
        if network_functions.connect():     # Проверяем, работает ли сервер
            file_from_user = bot.download_file(bot.get_file(message.document.file_id).file_path)  # Получаем объект 'bytes'
            name_of_file = str(bot.get_file(message.document.file_id).file_path)[9:]   # Иникальное имя файла, выданное тг
            address_file_from_user = "files_from_user" + name_of_file    # Адрес, куда будем сохранять файл
            with open(address_file_from_user, 'wb') as new_file:   # Создали и записали файл
                new_file.write(file_from_user)
            with open(address_file_from_user, 'rb') as file_to_send:   # Открываем файл и отправляем его
                import requests
                r = requests.post('https://urbanml.art/post/excel', files={'file': file_to_send})
                print("Файл успешно отправлен на сервер")
            src_result = "result_files" + name_of_file    # Адрес для ответа на post
            with open(src_result, 'wb') as result_file:   # Записываем полученный ответ на post
                result_file.write(r.content)
            with open(src_result, 'rb') as file_for_user:   # Открываем для отправки конечному пользователю
                bot.send_document(message.chat.id, file_for_user)
                print("Файл успешно отправлен пользователю")
            os.remove(address_file_from_user)   #
            os.remove(src_result)
        else:
            bot.send_message(message.chat.id, "К сожалению, произошла ошибка подключения к серверу :(")
    except Exception as ex:
        import logging
        logging.critical(ex)
        bot.send_message(message.chat.id, "Произошла ошибка обработки файла...")


bot.polling(none_stop=False, interval=0, timeout=20)
