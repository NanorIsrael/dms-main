import pika, json
from main import Product, db, app
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", port=5672))
channel = connection.channel()

# Ensure fair message distribution
channel.basic_qos(prefetch_count=1)

def callback(ch, method, properties, body):
    print('Recieved in main')
    try:
        logging.info(f"Content Type: {properties.content_type}")
        data = json.loads(body)
        logging.info(f"Received message: {data}")
        with app.app_context():
            if properties.content_type == 'product_created':
                product = Product(id=data['id'], title=data['title'], likes=data['likes'], image=data['image'])
                db.session.add(product)
                db.session.commit()
            if properties.content_type == 'product_updated':
                product = Product.query.get(data['id'])
                Product.title = data['title']
                Product.likes=data['likes']
                Product.image=data['image']
                db.session.commit()
            if properties.content_type == 'product_deleted':
                product = Product.query.get(data['id'])
                Product.title = data['title']
                Product.likes=data['likes']
                Product.image=data['image']
                db.session.commit()
    except Exception as e:
        print(f"Error in callback: {e}", flush=True)


    # Process and acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Declare queue
channel.queue_declare(queue="main")

# Consume messages
channel.basic_consume(queue="main", on_message_callback=callback, auto_ack=False)

print("Waiting for messages...")
channel.start_consuming()
channel.close()