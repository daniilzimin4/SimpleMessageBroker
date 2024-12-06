from flask import Flask, request, jsonify
import pika

app = Flask(__name__)

# RabbitMQ connection details
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'messages'

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    user_alias = data.get('user_alias')
    message_text = data.get('message_text')

    if not user_alias or not message_text:
        return jsonify({"error": "Invalid input"}), 400

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Ensure queue exists
    channel.queue_declare(queue=QUEUE_NAME)

    # Publish message
    message = {'user_alias': user_alias, 'message_text': message_text}
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=str(message))

    connection.close()
    return jsonify({"status": "Message sent!"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
