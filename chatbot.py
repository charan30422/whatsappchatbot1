import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Environment variables (set in Render)
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")


# ==============================
# Home Route (Test Server)
# ==============================
@app.route("/")
def home():
    return "WhatsApp Chatbot is Running 🚀"


# ==============================
# Webhook Verification (GET)
# ==============================
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403


# ==============================
# Receive Messages (POST)
# ==============================
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


# ==============================
# Chatbot Logic
# ==============================
def generate_reply(user_text):
    user_text = user_text.lower().strip()

    if user_text in ["hi", "hello"]:
        return (
            "Welcome to Ullas Support 🌟\n\n"
            "1️⃣ When is UEE exam?\n"
            "2️⃣ Exam centre details\n"
            "3️⃣ Registration status\n"
            "4️⃣ Attendance\n"
            "5️⃣ Scholarship\n"
            "6️⃣ Certificate status\n"
            "7️⃣ Renewal status"
        )

    elif user_text == "1":
        return "UEE exam date will be announced on the official website."
    elif user_text == "2":
        return "Exam centre details will be shared via your registered email."
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


# ==============================
# Send Message to WhatsApp
# ==============================
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

    response = requests.post(url, headers=headers, json=data)
    print("WhatsApp Response:", response.text)


# ==============================
# Required for Render
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)