import smtplib
import pika
import ast

RABBITMQ_HOST = 'localhost'
INPUT_QUEUE = 'screaming_messages'

EMAIL_ADDRESS = 'your_test_email@gmail.com'
EMAIL_PASSWORD = 'your_password'

def publish_service(ch, method, properties, body):
    message = ast.literal_eval(body.decode())

    email_body = f"Message from {message['user_alias']}:\n\n{message['message_text']}"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(
            EMAIL_ADDRESS,
            EMAIL_ADDRESS,  # Replace with your team's email
            f"Subject: New Message\n\n{email_body}"
        )
    print(f"Email sent: {email_body}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=INPUT_QUEUE)
    channel.basic_consume(queue=INPUT_QUEUE, on_message_callback=publish_service, auto_ack=True)
    print("Publish Service started...")
    channel.start_consuming()

if __name__ == '__main__':
    main()
