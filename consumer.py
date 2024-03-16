import os
import sys

import pika

from email_send_model import Email_Send_To_Customer

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    queue_name = 'email_send_queue'
    channel.queue_declare(queue=queue_name, durable=True)

    
    def callback(ch, method, properties, body):
        pk = body.decode()
        customer = Email_Send_To_Customer.objects(id=pk, send=False).first()
        if customer:
            customer.update(set__send=True)
            print(f"Email to {customer['fullname']} has been sent")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
