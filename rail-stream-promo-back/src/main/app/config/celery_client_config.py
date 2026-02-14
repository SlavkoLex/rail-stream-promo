import asyncio
import os
from celery import Celery
from celery.result import AsyncResult
from typing import Callable
from typing import Optional


#==============================
# To work in a Docker container
# (For Celery worker)
#==============================
if os.path.exists('/app'):
    from celery_task_schema import *
    from load_env_file import load_env_file
    load_env_file()


#=======================================
# To work in FastAPI app on OS or Docker
#=======================================
else:
    from .celery_task_schema import *
    from .load_env_file import load_env_file
    load_env_file()

class CustomCeleryClientManager:

    @classmethod
    def __get_tasks_from_celery_task_schema(cls) -> dict[str, Callable]:

        functions_map: dict[str, Callable] = {}

        for name, func in list(globals().items()):
            if callable(func) and func.__module__ == 'celery_task_schema':
                functions_map[str(name)] = func

        return functions_map
    
    @classmethod
    def __task_registration_in_specified_queue(cls, celery_client: Celery, link_task: Callable, key_task: str, queue: str) -> None:
        celery_client.task(link_task, name=key_task, queue=queue)

        for name in celery_client.tasks.keys():
            print("Celery_task: " + name)

    @classmethod
    def __init_celery_obj(cls) -> Optional[Celery]:

        # Checking the running space (Docker or OS)
        if os.path.exists('/.dockerenv'):

            broker_url_used: Optional[str] = os.getenv('CELERY_BROKER_URL_DOCKER')
            backend_url_used: Optional[str] = os.getenv('CELERY_BACKEND_URL_DOCKER')
        else:
            broker_url_used: Optional[str] = os.getenv('CELERY_BROKER_URL_LOCALHOST')
            backend_url_used: Optional[str] = os.getenv('CELERY_BACKEND_URL_LOCALHOST')

        print("==========================================")
        print("Celery_broker = " + str(broker_url_used))
        print("Celery_backend = " + str(backend_url_used))
        print("==========================================")

        if (broker_url_used is None or 
            backend_url_used is None or 
            not broker_url_used.strip() or 
            not backend_url_used.strip()):
            
            missing: list[str] = []
            if broker_url_used is None or not broker_url_used.strip():
                missing.append('CELERY_BROKER_URL')
            if backend_url_used is None or not backend_url_used.strip():
                missing.append('CELERY_BACKEND_URL')
                
            print(f"Error: Missing or empty environment variables: {', '.join(missing)}")
            return None
        
        try:
            celery_instance: Celery = Celery('celery_tasker')
            celery_instance.conf.broker_url = broker_url_used
            celery_instance.conf.result_backend = backend_url_used
        except Exception as e:
            print(f"Error creating Celery instance: {e}")
            return None

        celery_instance.conf.update(

            # Celery result sets
            result_backend=backend_url_used,
            result_expires=3600,
            result_persistent=True,
            task_track_started=True,
             task_time_limit=1800,
             task_soft_time_limit=1200,

            # Broker settings via Kombu (by default, because when creating a Celery object, Kombu is automatically created)
            broker_pool_limit=10,  
            broker_heartbeat=120, 
            broker_connection_timeout=4.0,
            broker_connection_retry=True,
            broker_connection_max_retries=3,
            
            # Kombu Transport Settings
            broker_transport_options={
                'visibility_timeout': 3600, 
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

        for key, value in CustomCeleryClientManager.__get_tasks_from_celery_task_schema().items():
            CustomCeleryClientManager.__task_registration_in_specified_queue(celery_instance, value, key, 'default')

        return celery_instance
    


    def __init__(self):
        self.__celry_client: Optional[Celery] = CustomCeleryClientManager.__init_celery_obj()

    #=======================================
    # get a celery object from Celery manager
    #=======================================
    def get_celery_object(self) -> Optional[Celery]:
        return self.__celry_client
    
    #=======================================
    #waiting for the result of the task
    #=======================================
    async def wait_task_result(self, task_id: str, timeout: int = 30):
        result: AsyncResult = self.__celry_client.AsyncResult(task_id)

        start_time = asyncio.get_event_loop().time()
        while not result.ready():
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError(f"Timeout after {timeout}s")
            await asyncio.sleep(0.5)
        
        if result.successful():
            return result.result
        else:
            raise Exception(f"Task failed: {result.traceback}")
    
    

#=======================
# celery worker object initialization rule
#=======================
if os.path.exists('/app'):                     
    app: Optional[Celery] = CustomCeleryClientManager().get_celery_object()

else:
    print("===============================")
    print("Processing of the Celery module within the FastAPI application; Celery object not initialized")
    print("===============================")