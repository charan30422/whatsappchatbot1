import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# Home route (to check server running)
@app.route("/")
def home():
    return "WhatsApp Chatbot is Running 🚀"

# Webhook verification
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

# Receive messages
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message["text"]["body"]

        reply = generate_reply(text)
        send_message(sender, reply)

    except Exception as e:
        print("Error:", e)

    return "OK", 200

# Chatbot menu logic
def generate_reply(user_text):
    user_text = user_text.lower().strip()

    if user_text in ["hi", "hello", "hey"]:
        return (
            "Welcome to Ullas Support! 🌟\n\n"
            "Please choose an option:\n\n"
            "1️⃣ When is our UEE exam?\n"
            "2️⃣ UEE exam centre details\n"
            "3️⃣ Registration status\n"
            "4️⃣ Attendance & eligibility\n"
            "5️⃣ Scholarship\n"
            "6️⃣ Certificate status\n"
            "7️⃣ Renewal Status"
        )

    elif user_text == "1":
        return "UEE exam date will be announced on the official website."

    elif user_text == "2":
        return "Exam centre details will be sent to your registered email."

    elif user_text == "3":
        return "You can check registration status in the student portal."

    elif user_text == "4":
        return "Minimum 75% attendance is required."

    elif user_text == "5":
        return "Scholarship information is available in the portal."

    elif user_text == "6":
        return "Certificate status will be updated after results."

    elif user_text == "7":
        return "Renewal status is available in your dashboard."

    else:
        return "Please type 'Hi' to see the menu."

# Send message back to WhatsApp
def send_message(to, message):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=data)

if __name__ == "__main__":
    app.run(port=5000)