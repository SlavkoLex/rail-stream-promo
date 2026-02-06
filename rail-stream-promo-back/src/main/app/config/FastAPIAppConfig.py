from fastapi import FastAPI
from contextlib import asynccontextmanager

from . CeleryClientConfig import app

from endpoints.OrderEndpoint import order_router


@asynccontextmanager
async def lifespan(app_fastapi):

    #============================
    # Monitoring of the lifecycle 
    # MongoDB object
    #============================
    # .
    # .
    # .

    #============================
    # Monitoring of the lifecycle  
    # Celery object
    #============================
    app_fastapi.state.celery = app
    
    yield
    
    #============================
    # Close Celery Connections
    #============================
    if hasattr(app, 'close'):
        app.close()



app_fastapi = FastAPI(lifespan=lifespan)


#============================
# Endpoint registration
#============================
app_fastapi.include_router(order_router)
