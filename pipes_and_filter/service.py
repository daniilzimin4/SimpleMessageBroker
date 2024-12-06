from multiprocessing import Process, Queue
import smtplib
import time


STOP_WORDS = {'bird-watching', 'ailurophobia', 'mango'}
EMAIL_ADDRESS = 'your_test_email@gmail.com'
EMAIL_PASSWORD = 'your_password'


def rest_api_service(input_queue):
    messages = [
        {"user_alias": "User1", "message_text": "This is a normal message."},
        {"user_alias": "User2", "message_text": "This is a mango test."},
        {"user_alias": "User3", "message_text": "Hello, I have ailurophobia."},
        {"user_alias": "User4", "message_text": "Bird-watching is fun!"},
        {"user_alias": "User5", "message_text": "Just a regular message here."},
        {"user_alias": "User6", "message_text": "Completely fine text without banned words."},
    ]
    for message in messages:
        print(f"[REST API] Received message: {message}")
        input_queue.put(message)
        time.sleep(1)


def filter_service(input_queue, output_queue):
    while True:
        message = input_queue.get()
        if any(word in message["message_text"] for word in STOP_WORDS):
            print(f"[Filter Service] Message blocked: {message}")
        else:
            print(f"[Filter Service] Message passed: {message}")
            output_queue.put(message)


def screaming_service(input_queue, output_queue):
    while True:
        message = input_queue.get()
        message["message_text"] = message["message_text"].upper()
        print(f"[SCREAMING Service] Processed message: {message}")
        output_queue.put(message)


def publish_service(input_queue):
    while True:
        message = input_queue.get()
        email_body = f"Message from {message['user_alias']}:\n\n{message['message_text']}"
        print(f"[Publish Service] Sending email:\n{email_body}")
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(
                    EMAIL_ADDRESS,
                    EMAIL_ADDRESS,
                    f"Subject: New Message\n\n{email_body}"
                )
            print("[Publish Service] Email sent successfully.")
        except Exception as e:
            print(f"[Publish Service] Failed to send email: {e}")


if __name__ == "__main__":
    queue_rest_to_filter = Queue()
    queue_filter_to_screaming = Queue()
    queue_screaming_to_publish = Queue()

    processes = [
        Process(target=rest_api_service, args=(queue_rest_to_filter,)),
        Process(target=filter_service, args=(queue_rest_to_filter, queue_filter_to_screaming)),
        Process(target=screaming_service, args=(queue_filter_to_screaming, queue_screaming_to_publish)),
        Process(target=publish_service, args=(queue_screaming_to_publish,)),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
