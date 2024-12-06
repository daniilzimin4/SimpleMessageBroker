from locust import HttpUser, task, between
import random

MESSAGES = [
    {"user_alias": "User1", "message_text": "This is a normal message."},
    {"user_alias": "User2", "message_text": "This is a mango test."},
    {"user_alias": "User3", "message_text": "Hello, I have ailurophobia."},
    {"user_alias": "User4", "message_text": "Bird-watching is fun!"},
    {"user_alias": "User5", "message_text": "Just a regular message here."},
    {"user_alias": "User6", "message_text": "Completely fine text without banned words."}
]

class MessageSender(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def send_normal_message(self):
        message = random.choice([msg for msg in MESSAGES if "mango" not in msg["message_text"]
                                 and "ailurophobia" not in msg["message_text"]
                                 and "bird-watching" not in msg["message_text"]])
        self.client.post(
            "/send",
            json=message
        )

    @task(1)
    def send_banned_message(self):
        message = random.choice([msg for msg in MESSAGES if "mango" in msg["message_text"]
                                 or "ailurophobia" in msg["message_text"]
                                 or "bird-watching" in msg["message_text"]])
        self.client.post(
            "/send",
            json=message
        )
