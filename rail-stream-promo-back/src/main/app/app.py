import os
import sys
from typing import Optional
import uvicorn
from config.fast_api_app_config import app_fastapi
from config.load_env_file import load_env_file
from services.tools.env_var_checker import env_var_check

#========================
# Dynamically defining and 
# adding the project's root 
# directory to the Python path
#========================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, PROJECT_ROOT)

if __name__ == "__main__":
    
    #===========================================
    # reading and installing variable environments
    #===========================================
    load_env_file()


    if os.path.exists('/.dockerenv'):
        server_host: Optional[str] = os.getenv("UVICORN_SERVER_HOST_DOCKER")
        server_port_row: Optional[str] = os.getenv("UVICORN_SERVER_PORT")
    else:
        server_host: Optional[str] = os.getenv("UVICORN_SERVER_HOST")
        server_port_row: Optional[str] = os.getenv("UVICORN_SERVER_PORT")

    if not env_var_check(server_host, server_port_row):
        print("Error reading Uvicorn env variables!!")
        sys.exit(1)
        
    try:
        server_port: int = int(server_port_row) 
    except ValueError:
        print(f"Error: Uvicorn PORT_NOTIFIER must be integer, got {server_port_row}")
        sys.exit(1)

    uvicorn.run(
        app_fastapi,
        host = server_host, 
        port = server_port,

    )