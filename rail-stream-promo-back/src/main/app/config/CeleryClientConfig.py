from celery import Celery
import os

from CeleryTaskSchema import *
from LoadEnvFile import load_env_file

class CustomCeleryClient:

    @classmethod
    def __get_tasks_from_celery_task_schema(cls):
        functions_map = {}
        for name, func in list(globals().items()):
            if callable(func) and func.__module__ == 'CeleryTaskSchema':
                functions_map[str(name)] = func
        return functions_map
    
    @classmethod
    def __task_registration_in_specified_queue(cls, clery_client, link_task, key_task, queue):
        # TODO: Добавить проверку, что передаваемый объет taskLink является ссылкой на ф-цию
        clery_client.task(link_task, name=key_task, queue=queue)


    @classmethod
    def __init_celery_obj(cls):

        #===========================================
        # Установка переменных окружения
        load_env_file()

        # Проверка запускаемого пространтсва (Docker или OS)
        if os.path.exists('/.dockerenv'):
            broker_url_used = os.getenv('CELERY_BROKER_URL_DOCKER')
            backend_url_used = os.getenv('CELERY_BACKEND_URL_DOCKER')
        else:
            broker_url_used = os.getenv('CELERY_BROKER_URL_LOCALHOST')
            backend_url_used = os.getenv('CELERY_BACKEND_URL_LOCALHOST')
        #===========================================

        celeryInstance = Celery(
            'celery_tasker',
            broker = broker_url_used,
            backend = backend_url_used
        )

        celeryInstance.conf.update(

            # Настройки брокера через Kombu (по умолчанию т.к. при создании об-та Celery автоматом создается Kombu)
            broker_pool_limit=10,  # Максимум соединений в пуле
            broker_heartbeat=120,  # Keep-alive
            broker_connection_timeout=4.0,
            broker_connection_retry=True,
            broker_connection_max_retries=3,
            
            # Настройки Kombu транспорта
            broker_transport_options={
                'visibility_timeout': 3600,  # 1 час
                'fanout_prefix': True,
                'fanout_patterns': True,
                'socket_timeout': 5.0,
                'socket_connect_timeout': 5.0,
                'retry_on_timeout': True,
                'max_connections': 10,
                'health_check_interval': 30,
            },
            
            # Сериализация
            task_serializer='json',
            result_serializer='json',
            accept_content=['json'],
            result_accept_content=['json'],
            
            # Другие настройки
            timezone='Europe/Moscow',
            enable_utc=True,
        )

        for key, value in CustomCeleryClient.__get_tasks_from_celery_task_schema().items():
            CustomCeleryClient.__task_registration_in_specified_queue(celeryInstance, value, key, 'default')

        return celeryInstance


    def __init__(self):

        self.__celry_klient = CustomCeleryClient.__init_celery_obj()

    def get_celery_object(self):
        return self.__celry_klient
                     
app = CustomCeleryClient().get_celery_object()

    



