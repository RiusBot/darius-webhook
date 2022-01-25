import os
import logging
import json
import socket
import traceback
import datetime
import requests
from flask import Flask, request, jsonify, Response

from worker.config import configure_logging
from worker.services import validators
from worker.services.auth import fetch_backend_url_firestore, fetch_secret_token_firestore


configure_logging()
app = Flask(__name__)


@app.route("/_health", methods=["GET"])
def health_check():
    return Response(
        json.dumps({"status": "available"}),
        status=200,
        mimetype="application/json",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": 0,
        },
    )

@app.route("/webhook/<uid>", methods=["POST"])
@validators.webhook_validator
def webhook(uid):
    try:
        post_data = request.get_json()
        url = fetch_backend_url_firestore()
        endpoint = f"{url}/api/v1/execute_webhook_signal"
        token = fetch_secret_token_firestore()
        headers = {"Authorization": f"Bearer {token}"}

        post_data["message_timestamp"] = datetime.datetime.now().timestamp()
        post_data["recieve_timestamp"] = datetime.datetime.now().timestamp()
        post_data["content"] = ""
        post_data["channel"] = "WEBHOOK"
        post_data["uid"] = uid

        response = requests.post(
            endpoint,
            json=post_data,
            headers=headers
        )
        try:
            result = response.json()
        except Excetion:
            result = {'result': response.text}

        logging.info(json.dumps(result, indent=4))
        return jsonify(result), 200
    except Exception as e:
        logging.error(str(e))
        logging.exception("")
        # traceback.format_exc()
        return jsonify({"error_message": str(e)}), 500
    
    
@app.route("/", methods=["POST"])
@validators.main_validator
def main():

    try:
        post_data = request.get_json()
        current_price = post_data.get("current_price")
        sentiment_stats = post_data.get("sentiment_stats")
        sentiment_status = post_data.get("sentiment_status")
        rolling_apy = post_data.get("rolling_apy")
        action = post_data.get("action")
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M (UTC+0)")
        
        rolling_apy = float(rolling_apy)
        sentiment_stats = float(sentiment_stats)
        current_price = float(current_price)
        
        emoji = "🔥" if sentiment_status == "Overheated" else "😭"
        rolling_apy_text = f"*BTC Rolling APY%:* {rolling_apy:.1f}%\n"
        sentiment_stats_text = f"*Sentiment Stats:* {sentiment_stats:.1f}\n"
        sentiment_status_text = f"*Status:* {emoji}{sentiment_status}\n"
        current_price_text = f"*BTC Price:* {current_price:.2f}\n"
        action_text = f"*Action:* {action}\n"
        time_text = f"*Time:* {time}\n"
        msg = rolling_apy_text + sentiment_stats_text + sentiment_status_text + current_price_text + action_text + time_text
        
        chat_id = os.environ.get("chat_id")
        auth_token = os.environ.get("auth_token")
        
        telegram_endpoint = f"https://api.telegram.org/bot{auth_token}/sendMessage"
        params = {
            "chat_id": chat_id,
            "parse_mode": "Markdown",
            "text": msg,
        }
        response = requests.get(
            telegram_endpoint,
            params=params
        )
        if response.status_code != 200:
            raise Exception(response.text)
        
        return jsonify(params), 200
    except Exception as e:
        logging.error(str(e))
        logging.exception("")
        # traceback.format_exc()
        return jsonify({"error_message": str(e)}), 500


if __name__ == "__main__":
    app.run()
