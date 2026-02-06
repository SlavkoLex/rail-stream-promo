from celery import Celery
import os

#==============================
# To work in a Docker container
# (For Celery worker)
#==============================
if os.path.exists('/.dockerenv'):
    from CeleryTaskSchema import *
    from LoadEnvFile import load_env_file

#==============================
# To work in FastAPI app
#==============================
else:
    from .CeleryTaskSchema import *
    from .LoadEnvFile import load_env_file


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
        clery_client.task(link_task, name=key_task, queue=queue)

        for k in clery_client.tasks.keys():
            print(k)


    @classmethod
    def __init_celery_obj(cls):

        #===========================================
        # reading and installing variable environments
        load_env_file()

        # Checking the running space (Docker or OS)
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

            # Broker settings via Kombu (by default, because when creating a Celery object, Kombu is automatically created)
            broker_pool_limit=10,  #
            broker_heartbeat=120, 
            broker_connection_timeout=4.0,
            broker_connection_retry=True,
            broker_connection_max_retries=3,
            
            # Kombu Transport Settings
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
            
            task_serializer='json',
            result_serializer='json',
            accept_content=['json'],
            result_accept_content=['json'],
            
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


    



