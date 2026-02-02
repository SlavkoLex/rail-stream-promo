from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import socket


def send_gmail_notification_about_order(**oreder_info):


    date_order = None
    client_email = None
    product = None
    organization = None 
    cient_number = None

    for key,value in oreder_info.items():
        
        match key:

            case "date_order": 
                date_order = value

            case "client_email":
                client_email = value

            case "product": 
                product = value

            case "organization":
                organization = value

            case "cient_number":
                cient_number = value

    #===================================================
    # Предполагается, что указанные преременные окружения настроены на ур-не OC
    # (Это стоит учитывать при развертывании Docker контейнера как с Celery так и с самим приложением)
    port = int(os.getenv('PORT_NOTIFIER'))
    host = os.getenv('HOST_NOTIFIER')

    sender_email = os.getenv('EMAIL_NOTIFIER')
    password = os.getenv('PASSWORD_NOTIFIER')
    receiver_email = sender_email

    #====================================================

    body = f"""Отправлена заявка от {date_order} \n
            * email клиента: {client_email} \n
            * Продукт: {product} \n
            * Организация: {organization}\n
            * Контактный номер: {cient_number}"""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Тема Письма"
    message.attach(MIMEText(body, "plain"))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    status = False

    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Порт {port} на {host} открыт")
            status = True

            #===============================================
            # Отправка сообщения на gmail
            #===============================================
            with smtplib.SMTP_SSL(host, port) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                
        else:
            print(f"Порт {port} на {host} закрыт или недоступен")
    except Exception as e:
        print(f"Ошибка проверки порта {port}: {e}")

    sock.close()
    return status

