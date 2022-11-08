import hashlib
from aiohttp import web
from time import time
from api import redis_userlogin_client
import bcrypt


def get_password_hash(user_pw):
    return bcrypt.hashpw(user_pw.encode('utf-8'), bcrypt.gensalt())


def check_passwd_match(pw1, pw2):
    return bcrypt.checkpw(pw1, pw2)


def authenticated(original_function):
    def wrapper(request):
        user_id = request.cookies.get('user_id')
        session_id = request.cookies.get('session_id')

        if not redis_userlogin_client.get(user_id):
            return web.Response(status=401)
        if redis_userlogin_client.get(user_id).decode('utf-8') != session_id:
            return web.Response(status=401)

        return original_function(request)
    return wrapper


def generate_session_id(user_id, user_pw):
    return hashlib.sha256(
        "#".join([user_id, user_pw, str(time())]).encode()
    ).hexdigest()
