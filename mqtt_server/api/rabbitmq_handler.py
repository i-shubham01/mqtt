from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import Optional
from mqtt_server.db.mongo import MongoDBHandler
from mqtt_server.rabbitmq.rabbitmq_listener import RabbitMQListener

router = APIRouter()
mongo = MongoDBHandler()
listener = RabbitMQListener(mongo)

@router.post("/start_consumer/")
async def start_consumer():
    """
    Endpoint to start consuming messages from RabbitMQ queue.
    """
    try:
        listener.start()
        return {"message": "RabbitMQ consumer started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop_consumer/")
async def stop_consumer():
    """
    Endpoint to stop consuming messages from RabbitMQ queue.
    """
    try:
        listener.stop()
        return {"message": "RabbitMQ consumer stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))