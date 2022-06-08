import logging
import requests
from worker.config import config
from worker.services.auth import fetch_secret_token_firestore


def send_to_execute(info: dict):
    token = fetch_secret_token_firestore()
    headers = {"Authorization": f"Bearer {token}"}

    symbol_list = info["symbol"]
    symbol_list = [] if symbol_list is None else symbol_list
    action = info["action"]
    for symbol in symbol_list:
        info["symbol"] = symbol.strip() if isinstance(symbol, str) else symbol
        logging.info(f"{symbol} {action} send to execute.")
        
        for endpoint in config["backend_endpoint"]:
            logging.info(f"{endpoint}")
            response = requests.post(endpoint, json=info, headers=headers)
            try:
                logging.info(str(response) + " " + json.dumps(response.json()))
            except Exception:
                logging.info(str(response) + " " + response.text)
            break  # dont send to stg
        
    logging.info("complete execute")
