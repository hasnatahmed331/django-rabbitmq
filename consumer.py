import pika
import json


def process_message(ch, method, properties, body):
    message = json.loads(body)
    send_welcome_email(message["email"])
    ch.basic_ack(delivery_tag=method.delivery_tag)


def send_welcome_email(email):
    # Your email sending logic here
    print(f"Sending welcome email to ({email})")


def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="student_queue", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="student_queue", on_message_callback=process_message)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    start_consumer()
