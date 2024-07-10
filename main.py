from mqtt_server.api.mqtt_handler import router as mqtt_router
from fastapi import FastAPI, HTTPException, Request
from mqtt_server.db.mongo import MongoDBHandler
from mqtt_server.rabbitmq.rabbitmq_listener import RabbitMQListener
from mqtt_server.api.mqtt_handler import router as mqtt_router
from mqtt_server.api.rabbitmq_handler import router as rabbit_router
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from mqtt_server.constants.constants import MongoCollections, RabbitMQQueues

app = FastAPI(
    title="RabbitMQ API",
    debug=True
)
app.include_router(mqtt_router, prefix="/api", tags=["MQTT"])
app.include_router(rabbit_router, prefix="/api", tags=["RabbitMQ"])

# MongoDB instance
mongo = MongoDBHandler()

# RabbitMQListener instance
listener = RabbitMQListener(mongo)
async def start_listener():
    listener.start()

# Function to stop listener asynchronously
async def stop_listener():
    listener.stop()


@app.on_event("startup")
async def on_startup():
    try:
        await start_listener()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def on_shutdown():
    try:
        await stop_listener()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log incoming requests.
    """
    print(f"Request received: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response sent: {response.status_code}")
    return response

