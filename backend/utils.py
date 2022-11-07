import hashlib
from time import time
from api import redis_userlogin_client
import bcrypt


def get_password_hash(user_pw):
    return bcrypt.hashpw(user_pw.encode('utf-8'), bcrypt.gensalt())


def check_passwd_match(pw1, pw2):
    return bcrypt.checkpw(pw1, pw2)


def is_valid_user(user_id, session_id):
    if not redis_userlogin_client.get(user_id):
        return False
    return redis_userlogin_client.get(user_id).decode('utf-8') == session_id


def generate_session_id(user_id, user_pw):
    return hashlib.sha256(
        "#".join([user_id, user_pw, str(time())]).encode()
    ).hexdigest()
