import pika


def get_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    return connection


def publish_message(queue, message):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),  # make message persistent
    )
    connection.close()
