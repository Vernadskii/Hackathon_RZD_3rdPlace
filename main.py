""" Функция для запуска """
import telebot
import passwords
bot = telebot.TeleBot(passwords.key)
src_res = ''


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Реакция на /start"""
    print(message)
    bot.send_message(message.chat.id, "Привет, " + str(message.from_user.first_name)
                 + ", это твой личный друг-аналитик!")
    user_functions.start(message.chat.id, bot)


from functions import user_functions
FUNCTIONS = dict(start=user_functions.start, download_excel=user_functions.download_excel,
                 about_prog=user_functions.about_prog, want=user_functions.want)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Обработик inline-кнопок"""
    try:
        if call.data == 'want':
            from functions import user_functions
            user_functions.want(call.message.chat.id, bot, src_res)
        else:
            FUNCTIONS[call.data](call.message.chat.id, bot)
    except Exception as ex:
        import logging
        logging.critical(ex)
        logging.critical(" Ошибка в callback_query_handler")


@bot.message_handler(content_types=['document'])
def send_doc(message):
    """ Функция приёма файлов и отправки ссылок на них серверу """
    try:
        bot.send_message(message.chat.id, "Теперь отправь мне второй...")
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
    bot.reply_to(message, "Файлы отправлены на вычислительный сервер. Ждём ответа...")
    import time
    time.sleep(2)
    import requests
    r = requests.post('https://urbanml.art/post/links', json={"file1": file_url1, "file2": file_url2 })
    import random
    import string
    letters = string.ascii_letters
    name_file_to_save = ''.join(random.choice(letters) for i in range(2))
    src_result = "result_files/Result_" + name_file_to_save + ".xlsx"
    with open(src_result, 'wb') as result_file:  # Записываем полученный ответ на post в папку result_files
        result_file.write(r.content)
    print("Файл сохранён")
    with open(src_result, 'rb') as file_for_user:  # Открываем для отправки конечному пользователю
        bot.send_document(message.chat.id, file_for_user)
    print("Файл успешно отправлен пользователю")
    global src_res
    src_res = src_result
    from functions import user_functions
    user_functions.do_you_wanna_send_email(message.chat.id, bot)


bot.polling(none_stop=False, interval=0, timeout=20)
