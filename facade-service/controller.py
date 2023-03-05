import httpx
import logging
import logging.config
from .message import Message
from urllib.parse import urljoin
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("facade-service")

MICRO_CONFIG = {
    "logging-service": "http://localhost:8001",
    "messages-service": "http://localhost:8002"
}

async def microservice_get(client, micro_name: str, path: str):
    response = await client.get(urljoin(MICRO_CONFIG[micro_name], path))
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=503, detail=f"Error when requesting {micro_name}: {response}")

@app.post("/facade_service")
async def facade_service_post(request: Request):
    msg = (await request.body()).decode().strip('"')
    async with httpx.AsyncClient() as client:
        response = await client.post(
            urljoin(MICRO_CONFIG["logging-service"], "log"),
            json=Message(msg).json(),
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=503, detail=f"Error when requesting logging-service: {response}")

@app.get("/facade_service")
async def facade_service_get():
    async with httpx.AsyncClient() as client:
        logging_resp = await microservice_get(client, "logging-service", "log")
        messages_resp = await microservice_get(client, "messages-service", "message")
    return logging_resp + ": " + messages_resp
