import random
from datetime import datetime
import pika
import json
import threading
import time
from config import BaseConfig
from mqtt_server.db.mongo import MongoDBHandler
from mqtt_server.constants.constants import MongoCollections, RabbitMQQueues


class RabbitMQListener:
    def __init__(self, mongo_instance: MongoDBHandler):
        self.mongo = mongo_instance
        self.connection = None
        self.channel = None
        self.consumer_thread = None
        self.retry_attempts = 3
        self.retry_delay = 3
        self.consumer_running = threading.Event()

    def connect(self):
        try:
            # parameters = pika.ConnectionParameters('localhost')
            parameters = pika.ConnectionParameters(host=BaseConfig.RABBITMQ_HOST,
                                                   port=BaseConfig.RABBITMQ_PORT)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            print('RabbitMQ connection established.')
        except pika.exceptions.AMQPConnectionError:
            print('Failed to connect to RabbitMQ. Retrying in 5 seconds...')
            time.sleep(5)
            self.connect()

    def start_consumer_thread(self):
        self.consumer_thread = threading.Thread(target=self._consume_messages)
        self.consumer_thread.start()

    def stop_consumer_thread(self):
        self.consumer_running.clear()  # Signal the consumer thread to stop

    def _consume_messages(self):
        self.channel.queue_declare(queue=RabbitMQQueues.MESSAGES)
        self.channel.basic_consume(queue=RabbitMQQueues.MESSAGES, on_message_callback=self.callback, auto_ack=True)
        print('RabbitMQ consumer started.')
        self.consumer_running.set()  # Signal that consumer is running
        while self.consumer_running.is_set():
            self.connection.process_data_events()
            self.consumer_running.wait(timeout=1)  # Adjust timeout as necessary

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        message['status'] = random.randrange(0, 7)
        self.mongo.insert_one(collection_name=MongoCollections.MESSAGES,document=message)
        print(f"Received and processed message: {message}")

    def push_message(self, routing_key: str, message: dict):
        retries = 0
        while retries < self.retry_attempts:
            try:
                if not self.channel or self.channel.is_closed:
                    self.connect()  # Reconnect if the channel is closed
                message_str = json.dumps(message)
                self.channel.basic_publish(exchange='', routing_key=routing_key, body=message_str)
                print(f"Sent message: {message}")
                return  # Exit the loop if message sent successfully
            except pika.exceptions.StreamLostError as e:
                print(f"Error occurred: {e}. Retrying...")
                retries += 1
                sleep(self.retry_delay)  # Wait before retrying
                continue
            except pika.exceptions.AMQPConnectionError as e:
                print(f"Error occurred: {e}. Retrying...")
                retries += 1
                sleep(self.retry_delay)  # Wait before retrying
                continue
        print("Failed to send message after retries.")

    def start(self):
        self.connect()
        self.start_consumer_thread()

    def stop(self):
        self.stop_consumer_thread()
        if self.consumer_thread:
            self.consumer_thread.join()  # Wait for consumer thread to terminate
        if self.connection:
            self.connection.close()
            print('RabbitMQ consumer stopped.')


