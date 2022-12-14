import sys
import logging
from aiohttp import web
sys.path.append('../')

# Q: 파이썬에서 이걸 좀 더 잘 처리할 수 있는 방법?
from config import APP_NAME
from api import mongo_db_client, redis_userlogin_client
from utils import generate_session_id, get_password_hash, \
    check_passwd_match, authenticated

routes = web.RouteTableDef()


@routes.post('/api/v1/signin')
async def signin(request):
    try:
        req_data = await request.json()
    except Exception as e:
        logging.error(e)
        return web.Response(status=400)

    user_id, user_pw = req_data['id'], req_data['pw']

    db_data = mongo_db_client[APP_NAME]['users'].find_one({
        'id': user_id
    })

    if not db_data or not check_passwd_match(
        user_pw.encode('utf-8'), db_data['pw']
    ):
        return web.Response(status=401)
    else:
        if redis_userlogin_client.get(req_data['id']):
            logging.info(f"'{user_id}' already logged in")

        session_id = generate_session_id(
            user_id,
            user_pw,
        )

        session_duration = 24 * 3600
        redis_userlogin_client.set(
            user_id,
            session_id,
            session_duration
        )

        res = web.Response(status=200)
        res.set_cookie(
            'session_id',
            session_id,
            httponly=True,
            secure=True,
            samesite=True,
            max_age=session_duration
        )

        res.set_cookie(
            'user_id',
            user_id,
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
        return web.Response(status=400)

    user_id = req_data['id']
    data = {
        'id': user_id,
        'pw': get_password_hash(req_data['pw'])
    }

    already_id_exist = mongo_db_client[APP_NAME]['users'].find_one({
        'id': user_id
    })

    if already_id_exist:
        return web.Response(status=409)

    try:
        mongo_db_client[APP_NAME]['users'].insert_one(data)
    except Exception as e:
        logging.error(e)
        return web.Response(status=500)

    return web.Response(status=200)


@routes.get('/api/v1/signout')
@authenticated
def signout(request):
    user_id = request.cookies.get('user_id')

    if not user_id:
        return web.Response(status=400)

    redis_userlogin_client.delete(user_id)

    res = web.Response(status=200)

    res.del_cookie('session_id')
    res.del_cookie('user_id')

    return res


@routes.get('/api/v1/check_login_session_is_valid')
@authenticated
def check_login_session_is_valid(_request):
    return web.Response(status=200)
