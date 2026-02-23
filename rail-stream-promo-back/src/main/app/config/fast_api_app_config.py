import os
import sys
from typing import AsyncIterator, Optional
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .celery_client_config import CustomCeleryClientManager
from .mongo_db_config import AsyncMongoDBCollection
from data.repository.order_repository import OrderRepository
from endpoints.order_endpoint import order_router
from utils.env_var_checker import env_var_check


@asynccontextmanager
async def lifespan(app_fastapi: FastAPI) -> AsyncIterator[None]:

    #============================
    # Monitoring of the lifecycle  
    # Celery manager object
    #============================
    celery_client_manager: CustomCeleryClientManager = CustomCeleryClientManager()

    if celery_client_manager.get_celery_object() is None:
        print("\nCelery initialization error!\n")
        sys.exit(1)

    app_fastapi.state.celery = celery_client_manager

    #============================
    # Monitoring of the lifecycle 
    # MongoDB object
    #============================
    if os.path.exists('/.dockerenv'):
        mongo_host: Optional[str] = os.getenv('MONGO_DOCKER_HOST') 
        mongo_port_row: Optional[str] = os.getenv('MONGO_PORT')
    else:
        mongo_host: Optional[str] = os.getenv('MONGO_HOST')
        mongo_port_row: Optional[str] = os.getenv('MONGO_PORT')

    mongo_user: Optional[str] = os.getenv('MONGODB_USER')
    mongo_pass: Optional[str] = os.getenv('MONGODB_PASSWORD')
    mongo_auth_src: Optional[str] = os.getenv('MONGO_AUTH_SRC')
    mongo_auth_mechanism: Optional[str] = os.getenv('MONGO_AUTH_MECHANISM')
    mongo_database: Optional[str] = os.getenv('MONGODB_DATABASE')
    mongo_collection: Optional[str] = os.getenv('MONGODB_ORDER_COLLECTION')

    if not env_var_check(
        mongo_host, 
        mongo_port_row, 
        mongo_user,
        mongo_pass,
        mongo_auth_src,
        mongo_auth_mechanism,
        mongo_database,
        mongo_collection):

        print("\nError reading Mongo env variables!!\n")
        sys.exit(1)

    try:
        mongo_port: int = int(mongo_port_row) 
    except ValueError:
        print(f"\nError: PORT_NOTIFIER must be integer, got {mongo_port_row}\n")
        sys.exit(1)
    
    try:
        mongo_collection_client: AsyncMongoDBCollection = AsyncMongoDBCollection.client_init(
            host = mongo_host,
            port = mongo_port, 
            user_name = mongo_user, 
            pwd = mongo_pass, 
            authSource = mongo_auth_src,
            authMechanism = mongo_auth_mechanism,
            db_name = mongo_database,
            collection_name = mongo_collection
        )
    except Exception as e:
        print(f"\nError creating MongoDB client: There may be a problem with the Mongo container -> {e}\n")
        sys.exit(1)

    if await mongo_collection_client.test_connect() is None:
        print("\n!!!!The request to the mongo container failed!!!\n")
        sys.exit(1)


    order_rep: OrderRepository = OrderRepository(mongo_collection_client.get_current_collection())

    app_fastapi.state.mongo_client_collection = mongo_collection_client
    app_fastapi.state.order_rep = order_rep
    
    yield
    
    #============================
    # Close Celery Connections
    #============================
    app_fastapi.state.celery.get_celery_object().close()

    #============================
    # Close Mongo Connections
    #============================
    app_fastapi.state.mongo_client_collection.close_current_connect()


app_fastapi: FastAPI = FastAPI(lifespan=lifespan)


#============================
# Endpoint registration
#============================
app_fastapi.include_router(order_router)
