from fastapi import APIRouter, HTTPException, Query, Request, Response
from datetime import datetime
from typing import Optional, Dict, Any
from mqtt_server.db.mongo import MongoDBHandler
from mqtt_server.rabbitmq.rabbitmq_listener import RabbitMQListener
from mqtt_server.constants.constants import MongoCollections, RabbitMQQueues
import json

router = APIRouter()
mongo = MongoDBHandler()
listener = RabbitMQListener(mongo)

@router.get('/message')
async def get_status_counts(
    response: Response,
    query: Optional[Dict[str, Any]] = None,
    skip: int = 0,
    limit: int = 10,
    sort_field: Optional[str] = None,
    sort_order: Optional[str] = "asc",
):
    """
    This endpoint returns the messages processed and the total number of messages in the database.
    :param response:
    :param query: can apply filters
    :param skip: number of records to skip
    :param limit: number of records to return
    :param sort_field: field to sort on
    :param sort_order: asc or desc
    :return:
    """
    try:
        parsed_query = json.loads(query) if query else {}
        total_count, counts = mongo.find(
            collection_name=MongoCollections.MESSAGES,
            skip=skip,
            query=query,
            limit=limit,
            sort_field=sort_field,
            sort_order=sort_order,
        )
        response.headers["X-Total-Count"] = str(total_count)
        return counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/message/send')
async def push_message(message: dict):
    """
    Endpoint to push a message to RabbitMQ queue.
    :param message: dict
    """
    try:
        message_str = json.dumps(message)
        listener.push_message(routing_key=RabbitMQQueues.MESSAGES, message=message)
        return {"message": "Message sent to RabbitMQ queue"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

