import pika


def get_connection():
    """
    Establishes a connection to RabbitMQ server.

    Returns:
        BlockingConnection: The connection object.
    """
    # Establish a blocking connection to RabbitMQ server.
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    return connection


def publish_message(queue, message):
    """
    Publishes a message to the specified queue.

    Args:
        queue (str): The name of the queue.
        message (str): The message to be sent.
    """
    # Get a connection to RabbitMQ server.
    connection = get_connection()
    # Create a channel.
    channel = connection.channel()
    # Declare a durable queue.
    channel.queue_declare(queue=queue, durable=True)
    # Publish the message to the specified queue.
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),  # Make message persistent
    )
    # Close the connection.
    connection.close()
