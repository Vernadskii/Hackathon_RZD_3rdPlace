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


def send_email(send_to, source, first_name):
    """ Функция для отправки файла на почту """
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email.mime.text import MIMEText
        from email.utils import formatdate
        from email import encoders
        import passwords
        msg = MIMEMultipart()
        msg['From'] = passwords.email_login
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = "Письмо из хакатона :)"
        msg.attach(MIMEText('Письмо с результатом анализа от пользователя ' + str(first_name)))

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(source, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=Report.xlsx')
        msg.attach(part)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(passwords.email_login, passwords.email_password)
        smtp.sendmail(passwords.email_login, send_to, msg.as_string())
        smtp.quit()
    except AssertionError as ex:
        import logging
        logging.warning(ex)