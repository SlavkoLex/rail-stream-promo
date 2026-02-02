from fastapi import FastAPI
from contextlib import asynccontextmanager

from CeleryClientConfig import app


@asynccontextmanager
async def lifespan(app: FastAPI):

    # TODO: Создать и настроить объекты Сelery, Mongo, Redis в соотв-щих .py файлах, а далее передать их 
    # в качестве атрибутов к созданному объекту state
    app.state.celery = app
    
    yield
    
    # Shutdown: закрываем подключения


app = FastAPI(lifespan=lifespan)

