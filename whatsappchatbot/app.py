# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# def send_whatsapp_message(to_number, message_text):
#     url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

#     headers = {
#         "Authorization": f"Bearer {ACCESS_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "messaging_product": "whatsapp",
#         "to": to_number,
#         "type": "text",
#         "text": {
#             "body": message_text
#         }
#     }

#     response = requests.post(url, headers=headers, json=payload)

#     print("Status Code:", response.status_code)
#     print("Response:", response.json())


# if __name__ == "__main__":
#     recipient_number = "919885479833"  # Replace with your number
#     message = "Hello 🚀 Sent from Cursor using WhatsApp Cloud API!"

#     send_whatsapp_message(recipient_number, message)





import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

PURPLE_FABRIC_API_URL = os.getenv("PURPLE_FABRIC_API_URL")
PURPLE_FABRIC_API_KEY = os.getenv("PURPLE_FABRIC_API_KEY")


# ===============================
# 1️⃣ WEBHOOK VERIFICATION
# ===============================

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified!")
        return challenge, 200
    else:
        return "Verification failed", 403


# ===============================
# 2️⃣ RECEIVE MESSAGE FROM WHATSAPP
# ===============================

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.json
    print("Incoming message:", data)

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        user_text = message["text"]["body"]

        print("User said:", user_text)

        # Call Purple Fabric
        pf_reply = call_purple_fabric(user_text)

        # Send reply back to WhatsApp
        send_whatsapp_message(sender, pf_reply)

    except Exception as e:
        print("Error:", str(e))

    return "OK", 200


# ===============================
# 3️⃣ CALL PURPLE FABRIC API
# ===============================

def call_purple_fabric(user_message):

    headers = {
        "Authorization": f"Bearer {PURPLE_FABRIC_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "message": user_message
    }

    try:
        response = requests.post(
            PURPLE_FABRIC_API_URL,
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return response.json().get("reply", "No reply from Purple Fabric")
        else:
            return "Purple Fabric error."

    except Exception as e:
        print("Purple Fabric Error:", str(e))
        return "Service unavailable."


# ===============================
# 4️⃣ SEND MESSAGE BACK TO WHATSAPP
# ===============================

def send_whatsapp_message(to, message_text):

    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("WhatsApp response:", response.json())


# ===============================
# START SERVER
# ===============================

if __name__ == "__main__":
    app.run(port=5000, debug=True)