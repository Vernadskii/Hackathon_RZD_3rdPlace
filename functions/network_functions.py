"""Модуль для работы с сетью и т.д"""


def connect():
    """ Функция, проверяющая состояние сервера
        Возвращает False, если статус != 200 и True, если статус == 200"""
    try:
        import requests
        r = requests.get('https://urbanml.art/hello/username')
        assert r.status_code == 200, "Error with connect to server with status " \
                                     ""+str(r.status_code)+". Ask Vlad to check server"
        print("Сервер работает")
        return True
    except AssertionError as ex:
        import logging
        logging.warning(ex)
        return False
