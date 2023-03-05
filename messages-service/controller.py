import logging
import logging.config
from fastapi import FastAPI

app = FastAPI()

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("messages-service")

@app.get("/message")
async def get_message():
    return "messages-service is not implemented yet"
