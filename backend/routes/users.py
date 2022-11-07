# Q: 파이썬에서 이걸 좀 더 잘 처리할 수 있는 방법?
import sys
import logging
import hashlib
from aiohttp import web
sys.path.append('../')

from config import APP_NAME
from api import mongo_db_client, redis_userlogin_client
from utils import is_valid_user, generate_session_id

routes = web.RouteTableDef()


@routes.post('/api/v1/signin')
async def signin(request):
    try:
        req_data = await request.json()
    except Exception as e:
        logging.error(e)
        return web.Response(status=400, reason=e.__cause__)

    data = {
        'id': req_data["id"],
        'pw': hashlib.sha256(req_data["pw"].encode()).hexdigest()
    }

    db_data = mongo_db_client[APP_NAME]['users'].find_one({
        'id': data['id']
    })

    if not db_data or not (
        data['id'] == db_data['id'] and data['pw'] == db_data['pw']
    ):
        return web.Response(status=401)
    else:
        if redis_userlogin_client.get(req_data["id"]):
            logging.info(f"'{req_data['id']}' already logged in")

        # id, pw, 로그인 시간으로 session_id 생성해, 브라우저에 쿠키로 전달 (set-cookie)
        session_id = generate_session_id(
            user_id=req_data['id'],
            user_pw=req_data['pw'],
        )

        session_duration = 24 * 3600
        redis_userlogin_client.set(
            req_data["id"],
            session_id,
            session_duration
        )

        res = web.Response(status=200)
        res.set_cookie(
            "session_id",
            session_id,
            httponly=True,
            secure=True,
            samesite=True,
            max_age=session_duration
        )

        res.set_cookie(
            "user_id",
            data['id'],
            httponly=False,
            secure=True,
            samesite=True,
            max_age=session_duration
        )
        return res


@routes.post('/api/v1/signup')
async def signup(request):
    try:
        req_data = await request.json()
    except Exception as e:
        logging.error(e)
        return web.Response(status=400, reason=e.__cause__)

    data = {
        'id': req_data["id"],
        'pw': hashlib.sha256(req_data["pw"].encode()).hexdigest()
    }

    already_id_exist = mongo_db_client[APP_NAME]['users'].find_one({
        'id': data['id']
    })

    if already_id_exist:
        return web.Response(status=409)

    try:
        mongo_db_client[APP_NAME]['users'].insert_one(data)
    except Exception as e:
        logging.error(e)
        return web.Response(status=500, reason=e.__cause__)

    return web.Response(status=200)


@routes.get('/api/v1/signout')
def signout(request):
    user_id = request.cookies.get('user_id')
    if not user_id:
        return web.Response(status=400)

    redis_userlogin_client.delete(user_id)

    res = web.Response(status=200)
    return res


@routes.get('/api/v1/ping')
def check_login_session_is_valid(request):
    user_id = request.cookies.get('user_id')
    session_id = request.cookies.get('session_id')

    if not is_valid_user(user_id=user_id, session_id=session_id):
        return web.Response(status=401)

    return web.Response(status=200)
