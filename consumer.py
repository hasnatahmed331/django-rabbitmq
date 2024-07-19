import pika
import json
import django
from django.core.mail import send_mail
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enrollement.settings")
django.setup()


def process_message(ch, method, properties, body):
    """
    Callback function to process a received message from the queue.

    Args:
        ch (BlockingChannel): The channel object.
        method (Method): Method frame with delivery info.
        properties (BasicProperties): Properties of the message.
        body (bytes): The message body.
    """
    # Load the message body (which is in JSON format) into a dictionary.
    message = json.loads(body)
    # Call the function to send a welcome email using the email from the message.
    send_welcome_email(message["email"])
    # Acknowledge the message so that it is removed from the queue.
    ch.basic_ack(delivery_tag=method.delivery_tag)


def send_welcome_email(email):
    """
    Simulates sending a welcome email to the given email address.

    Args:
        email (str): The email address to send the welcome email to.
    """
    send_mail(
        "Welcome Email",
        "Welcome To your School",
        "hasnatahmed331@gmail.com",
        ["hasnatahmed331@gmail.com"],
        fail_silently=False,
    )


def start_consumer():
    """
    Starts the RabbitMQ consumer to listen for messages on the 'student_queue' queue.
    """
    # Establish a connection to RabbitMQ server.
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    # Create a channel.
    channel = connection.channel()
    # Declare a durable queue named 'student_queue'.
    channel.queue_declare(queue="student_queue", durable=True)
    # Ensure the consumer does not receive more than one message at a time.
    channel.basic_qos(prefetch_count=1)
    # Start consuming messages from the queue with the specified callback function.
    channel.basic_consume(queue="student_queue", on_message_callback=process_message)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    # Enter a blocking loop that waits for data and runs callbacks when messages are received.
    channel.start_consuming()


if __name__ == "__main__":
    start_consumer()
