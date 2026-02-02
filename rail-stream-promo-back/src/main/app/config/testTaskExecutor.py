import datetime
from CeleryClientConfig import app

#====================================
# Тестовая проверка работы Celery, Reis, Docker
#====================================
if __name__ == '__main__':
    app.send_task(
        'send_gmail_notification_about_order', 
        args=None, date_order=datetime.datetime.now(), client_email="@mail", product="Sensor")
    
