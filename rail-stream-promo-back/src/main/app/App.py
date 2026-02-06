import os
import sys
import uvicorn
from config.FastAPIAppConfig import app_fastapi


#========================
# Dynamically defining and 
# adding the project's root 
# directory to the Python path
#========================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, PROJECT_ROOT)


if __name__ == "__main__":

    uvicorn.run(
        app_fastapi,
        host = os.getenv("UVICORN_SERVER_HOST"), 
        port = int(os.getenv("UVICORN_SERVER_PORT")),

    )