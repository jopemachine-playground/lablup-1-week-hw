import hashlib
from time import time
from api import redis_userlogin_client


def is_valid_user(user_id, session_id):
    if not redis_userlogin_client.get(user_id):
        return False
    return redis_userlogin_client.get(user_id).decode('utf-8') == session_id


def generate_session_id(user_id, user_pw):
    return hashlib.sha256(
        "#".join([user_id, user_pw, str(time())]).encode()
    ).hexdigest()
