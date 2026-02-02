import uvicorn
from config.FastAPIAppConfig import app

if __name__ == "__main__": # Брать значения из .env файла
    uvicorn.run(
        app,
        host="127.0.0.1", 
        port=8000,
        reload=True,      # только для разработки
        workers=1         # для продакшена можно увеличить
    )