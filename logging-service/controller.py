import logging
import logging.config
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("logging-service")

messages = dict()

@app.get("/log")
async def list_log():
    return f'[{", ".join(messages.values())}]'

class MessageBody(BaseModel):
    text: str
    uuid: str

@app.post("/log")
async def post_message(message: MessageBody):
    logger.info(f"Message{{{message}}}")
    messages[message.uuid] = message.text
