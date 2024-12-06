import requests

response = requests.post(
    "http://127.0.0.1:5000/send",
    json={"user_alias": "Alice", "message_text": "Hello, this is a mango test!"}
)

print(response.json())
