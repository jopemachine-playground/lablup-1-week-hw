import hashlib
from api import redis_userlogin_client

def is_valid_user(user_id, session_id):
    if redis_session_id := redis_userlogin_client.get(user_id):
        return session_id == redis_session_id
    return False

def generate_session_id(user_id, user_pw):
    return hashlib.sha256("#".join([user_id, user_pw, str(time())]).encode()).hexdigest()
