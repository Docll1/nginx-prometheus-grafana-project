from flask import Flask, request
import os, requests

app = Flask(__name__)

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

@app.route("/send_test")
def send_test():
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        return "Telegram env vars not set", 500

    text = "Test message from Telegram proxy"
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={TG_CHAT_ID}&text={text}"
    r = requests.get(url)
    return f"Sent: {r.text}"

@app.route("/send_alert", methods=["POST"])
def send_alert():
    data = request.get_json()
    print(data)  # можно оставить для отладки

    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        return "Telegram env vars not set", 500

    # Формируем текст алерта
    text = f"ALERT:\n{data}"
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": text}
    r = requests.post(url, json=payload)
    print(r.text)  # логируем ответ от Telegram
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
