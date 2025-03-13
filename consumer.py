import pika, json
from main import Product, db
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", port=5672))
channel = connection.channel()

# Declare queue
channel.queue_declare(queue="main")

# Ensure fair message distribution
channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    try:
        logging.info(f"Received message: {body}")
        logging.info(f"Content Type: {properties.content_type}")
        if properties.content_type == 'product_created':
            pass
    except Exception as e:
        print(f"Error in callback: {e}", flush=True)


    # Process and acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consume messages
channel.basic_consume(queue="main", on_message_callback=callback, auto_ack=False)

print("Waiting for messages...", flush=True)
channel.start_consuming()
