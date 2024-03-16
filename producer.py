import json
from datetime import datetime

import pika
from faker import Faker

from email_send_model import Email_Send_To_Customer

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

exchange = 'Send email exchange'
queue_name = 'email_send_queue'

channel.exchange_declare(exchange=exchange, exchange_type="direct")
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange, queue=queue_name)


def create_tasks(nums: int):
    for i in range(nums):
        customer = Email_Send_To_Customer(fullname=fake.name(), email=fake.email()).save()

        channel.basic_publish(
            exchange=exchange,
            routing_key=queue_name,
            body=str(customer.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    connection.close()


if __name__ == "__main__":
    fake = Faker()
    create_tasks(10)
