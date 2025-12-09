
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests # Added for Telegram API
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors
        print("Telegram message sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

@app.route("/api/contact", methods=["POST"])
def receive_contact_form():
    if request.is_json:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")

        print(f"Received Contact Form Submission:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")

        telegram_message = (
            f"<b>New Contact Form Submission:</b>\n\n"
            f"<b>Name:</b> {name}\n"
            f"<b>Email:</b> {email}\n"
            f"<b>Subject:</b> {subject}\n"
            f"<b>Message:</b>\n{message}"
        )
        send_telegram_message(telegram_message)

        response_message = {"message": "Contact form submitted successfully!", "received_data": data}
        return jsonify(response_message), 200
    else:
        return jsonify({"message": "Request must be JSON"}), 400

@app.route("/", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello from Flask backend!"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
