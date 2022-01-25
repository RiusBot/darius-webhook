import os
import logging
import functools
from firebase_admin import firestore, auth, initialize_app


initialize_app()
usingProjectId = os.getenv('project_id', 'local')


@functools.lru_cache(maxsize=None)
def fetch_tg_token_firestore():
    db = firestore.Client()
    Secret = db.collection("config").document("backend").get().to_dict()
    Token = Secret['tg_token']
    return Token


@functools.lru_cache(maxsize=None)
def fetch_secret_token_firestore():
    db = firestore.Client()
    Secret = db.collection("config").document("backend").get().to_dict()
    Token = Secret['auth_token']
    return Token


@functools.lru_cache(maxsize=None)
def fetch_backend_url_firestore():
    db = firestore.Client()
    config = db.collection("config").document("backend").get().to_dict()
    url = config['BACKEND_URL']
    return url


@functools.lru_cache(maxsize=None)
def fetch_backend_url_firestore():
    db = firestore.Client()
    Secret = db.collection("config").document("backend").get().to_dict()
    url = Secret['BACKEND_URL']
    return url


def check_client_access(json_payload: dict):
    # TODO HERE
    try:
        clientUserIdToken = json_payload.get('idToken')
        if clientUserIdToken is None or clientUserIdToken == '':
            return False
        decoded_token = auth.verify_id_token(clientUserIdToken, check_revoked=True)
        uid = decoded_token.get('uid')
        return uid
    except Exception:
        logging.error("exception when dealing with check_client_access token")
        logging.exception("")
        return False


def check_server_access(json_payload):
    try:
        Token = fetch_secret_token()
        requestToken = json_payload.get('token')
        if not Token or not requestToken:
            return False
        return Token == requestToken
    except Exception:
        logging.error("exception when dealing with check_server_access token")
        return False


def authenticate(json_payload):
    if usingProjectId != "local":
        if check_client_access(json_payload) is False:
            if check_server_access(json_payload) is False:
                return False
    return True
