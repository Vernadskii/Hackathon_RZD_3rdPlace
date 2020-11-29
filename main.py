""" Функция для запуска """
import telebot
import passwords
from telebot import types
bot = telebot.TeleBot(passwords.key)
src_res = ''
tree_of_steps = ''
top_tree_of_steps = ''


def rating_top(type_of_top, message_chat_id):
    try:
        global top_tree_of_steps
        top_tree_of_steps = ''
        aba = {'top_residue': 'residue', 'top_rate_norm': 'rate_norm', 'top_low_rate': 'low_rate',
               'top_up_rate': 'up_rate'}

        top_tree_of_steps += aba[type_of_top]
        print(top_tree_of_steps, "<-top_tree_of_steps")
        from functions import user_functions
        user_functions.month_top(message_chat_id, bot)
    except Exception as ex:
        import logging
        logging.critical(ex)
        print('ИскЛЮЧЕНИЕ!!!')


def rating_month(type_of_top, message_chat_id):
    global top_tree_of_steps
    try:
        print("rating_month")
        aba = {'top_April':'2020-04-01', 'top_May': '2020-05-01', 'top_June': '2020-06-01', 'top_July': '2020-07-01'}
        top_tree_of_steps += ("|"+ aba[type_of_top])
        length_tmp = len(top_tree_of_steps)
        print("rating_month")
        import requests
        r = requests.get('https://urbanml.art/get/raiting/' + top_tree_of_steps)
        import json
        print("rating_month")
        obj1 = json.loads(r.content)
        print(obj1)
        print("rating_month")
        obj2 = json.loads(obj1)
        print("rating_month")
        res = ''
        count = 0
        print(obj2)
        for key1 in obj2:
            count += 1
            res += str(count)+". "
            for i in obj2[key1].values():
                res += str(i)+"   "
            res += '\n'
        print(res)
        button1 = types.InlineKeyboardButton(text="📈 Новый ТОП", callback_data="rating")
        button2 = types.InlineKeyboardButton(text="🔙 Начало", callback_data="start")
        markup = types.InlineKeyboardMarkup()
        markup.row(button2, button1)
        bot.send_message(message_chat_id, res, reply_markup=markup)
    except Exception as ex:
        print(ex)
    top_tree_of_steps = top_tree_of_steps[:length_tmp]
    print(top_tree_of_steps)


def seriesss(series, message_chat_id):
    try:
        global tree_of_steps
        tree_of_steps = ''
        aba = {'DUAMATIK': 'ДУОМАТИК09-32GSM', 'RPB': 'РПБ-01', 'SHOM': 'ЩОМ-1200М', 'PMG': 'ПМГ'}
        print(aba[series])
        tree_of_steps += aba[series]
        from functions import user_functions
        user_functions.rate_months(message_chat_id, bot)
    except Exception as ex:
        print(ex)


def monthhh(month, message_chat_id):
    aba = {'April': '2020-04-01', 'May': '2020-05-01', 'June': '2020-06-01', 'July':'2020-07-01', 'August':'2020-08-01'}
    global tree_of_steps
    length_tmp = len(tree_of_steps)
    tree_of_steps += ("_"+aba[month])
    try:
        import requests
        r = requests.get('https://urbanml.art/get/plot/' + tree_of_steps)
        with open("docs/" + tree_of_steps + ".png", 'wb') as new_file:  # Создали и записали файл
            new_file.write(r.content)
        with open("docs/" + tree_of_steps + ".png", 'rb') as file_to_send:  # Открываем файл и отправляем его
            button1 = types.InlineKeyboardButton(text="📈 Новый график", callback_data="visualization_series")
            button2 = types.InlineKeyboardButton(text="🔙 Начало", callback_data="start")
            markup = types.InlineKeyboardMarkup()
            markup.row(button2, button1)
            bot.send_document(message_chat_id, file_to_send, reply_markup=markup)

    except Exception as ex:
        print(ex)
    tree_of_steps = tree_of_steps[:length_tmp]
    print(tree_of_steps)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Реакция на /start"""
    print(message)
    bot.send_message(message.chat.id, "Привет, " + str(message.from_user.first_name)
                 + ", это твой личный друг-аналитик!")
    user_functions.start(message.chat.id, bot)


from functions import user_functions
FUNCTIONS = dict(start=user_functions.start, reports=user_functions.reports,
                 download_excel=user_functions.download_excel, about_prog=user_functions.about_prog,
                 visualization=user_functions.visualization_series,
                 dont_want=user_functions.dont_want, rating=user_functions.rating)

FUNCTIONS_other_format = dict(DUAMATIK=seriesss, RPB=seriesss, SHOM=seriesss, PMG=seriesss,
                              April=monthhh, May=monthhh, June=monthhh, July=monthhh, August=monthhh)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Обработик inline-кнопок"""
    try:
        if call.data == 'top_residue': rating_top(call.data, call.message.chat.id)
        if call.data == 'top_rate_norm': rating_top(call.data, call.message.chat.id)
        if call.data == 'top_low_rate': rating_top(call.data, call.message.chat.id)
        if call.data == 'top_up_rate': rating_top(call.data, call.message.chat.id)
        if call.data == 'top_April': rating_month(call.data, call.message.chat.id)
        if call.data == 'top_May': rating_month(call.data, call.message.chat.id)
        if call.data == 'top_June': rating_month(call.data, call.message.chat.id)
        if call.data == 'top_July': rating_month(call.data, call.message.chat.id)
        if call.data == 'want':
            from functions import user_functions
            user_functions.want(call.message.chat.id, bot, src_res)
        try:
            FUNCTIONS[call.data](call.message.chat.id, bot)
        except:
            pass
        try:
            FUNCTIONS_other_format[call.data](call.data, call.message.chat.id)
        except:
            pass
    except Exception as ex:
        import logging
        logging.critical(ex)
        logging.critical(" Ошибка в callback_query_handler")



@bot.message_handler(content_types=['document'])
def send_doc(message):
    """ Функция приёма файлов и отправки ссылок на них серверу """
    try:
        from functions import network_functions
        if network_functions.connect():     # Проверяем, работает ли сервер
            bot.send_message(message.chat.id, "Теперь отправь мне второй (ССПС) ...")
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
    #import time
    #time.sleep(2)
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
