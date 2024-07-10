# MQTT-RabbitMQ-MongoDB Integration

## Project Description

This project involves developing a client-server script in Python to handle MQTT messages via RabbitMQ. The client script emits MQTT messages every second containing a field "status" with a random value in the range of 0-6. The server processes these messages and stores them in MongoDB. Additionally, the server provides an endpoint to accept start and end times and return the count of each status during the specified time range.

## Project Objectives

### MQTT Messaging Integration
- Implement MQTT messaging via RabbitMQ.
- Emit MQTT messages every second with a "status" field containing a random value between 0 and 6.

### Message Processing
- Develop a server script to process incoming MQTT messages.
- Store the processed messages in MongoDB.

### Data Retrieval Endpoint
- Create an endpoint to accept start and end times.
- Return the count of each status within the specified time range using MongoDB's aggregate pipeline.


## Installation and Setup

### Prerequisites
- Python 3.8+
- Docker
- Docker Compose

### Running with Docker

1. **Clone the Repository**
   ```bash
   git clone git@github.com:i-shubham01/mqtt.git
   cd mqtt-rabbitmq-mongodb
2. **Build and Run the Docker Containers
   ```bash
   docker-compose up --build

3. **Install Dependencies
   ```bash
   pip install -r requirements.txt
4. ** Set Required Envs
   ```text
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB = os.getenv('MONGO_DB', 'mqtt')
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')

5. ** Start the server
   ```bash
   uvicorn main:app --reload --port <port>
   

### Further Inhancement
```bash
- parameter validations
- Response schema
- logging implementation
- Bussiness logic for message processing
- Exception handling
- Middleware implementation
```
