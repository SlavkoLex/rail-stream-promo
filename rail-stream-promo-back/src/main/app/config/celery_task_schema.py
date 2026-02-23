from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import socket
import ssl
from typing import Optional


def send_gmail_notification_about_order(
        date_order: str, 
        client_email: str, 
        product: str, 
        organization: str, 
        cient_phone: str) -> bool:


    port_row: Optional[str] = os.getenv('PORT_NOTIFIER') 
    host: Optional[str] = os.getenv('HOST_NOTIFIER')

    sender_email: Optional[str] = os.getenv('EMAIL_NOTIFIER')
    password: Optional[str] = os.getenv('PASSWORD_NOTIFIER')
    receiver_email: Optional[str] = sender_email

    if not all([port_row, host, sender_email, password]):
        print("Error: Missing required environment variables")
        return False
    
    try:
        port: int = int(port_row) 
    except ValueError:
        print(f"Error: PORT_NOTIFIER must be integer, got {port_row}")
        return False
    
    receiver_email: str = sender_email

    body: str = f"""Отправлена заявка от {date_order} \n
            * email клиента: {client_email} \n
            * Продукт: {product} \n
            * Организация: {organization}\n
            * Контактный номер: {cient_phone}"""
    

    message: MIMEMultipart = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Заказ!"
    message.attach(MIMEText(body, "plain"))

    sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    status: bool = False

    try:
        result: int = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} : {host} is Open!")
            status = True

            #===============================================
            # Sending a message to gmail (Mail Collector)
            #===============================================
            with smtplib.SMTP(host, port) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                
        else:
            print(f"Port {port} : {host} closed or unavailable")
    except Exception as e:
        print(f"Port verification error! {port}: {e}")

    sock.close()
    return status