import pika
import ast

# RabbitMQ connection details
RABBITMQ_HOST = 'localhost'
INPUT_QUEUE = 'messages'
OUTPUT_QUEUE = 'filtered_messages'

STOP_WORDS = {'bird-watching', 'ailurophobia', 'mango'}

def filter_message(ch, method, properties, body):
    message = ast.literal_eval(body.decode())
    if not any(word in message['message_text'] for word in STOP_WORDS):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=OUTPUT_QUEUE)
        channel.basic_publish(exchange='', routing_key=OUTPUT_QUEUE, body=str(message))
        connection.close()

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=INPUT_QUEUE)
    channel.basic_consume(queue=INPUT_QUEUE, on_message_callback=filter_message, auto_ack=True)
    print("Filter Service started...")
    channel.start_consuming()

if __name__ == '__main__':
    main()
