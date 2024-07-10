import os
class BaseConfig:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB = os.getenv('MONGO_DB', 'mqtt')
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')