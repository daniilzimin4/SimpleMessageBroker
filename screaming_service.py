import pika
import ast

RABBITMQ_HOST = 'localhost'
INPUT_QUEUE = 'filtered_messages'
OUTPUT_QUEUE = 'screaming_messages'

def screaming_service(ch, method, properties, body):
    message = ast.literal_eval(body.decode())
    message['message_text'] = message['message_text'].upper()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=OUTPUT_QUEUE)
    channel.basic_publish(exchange='', routing_key=OUTPUT_QUEUE, body=str(message))
    connection.close()

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=INPUT_QUEUE)
    channel.basic_consume(queue=INPUT_QUEUE, on_message_callback=screaming_service, auto_ack=True)
    print("SCREAMING Service started...")
    channel.start_consuming()

if __name__ == '__main__':
    main()
