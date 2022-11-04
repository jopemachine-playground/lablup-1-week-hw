# Q: 파이썬에서 이걸 좀 더 잘 처리할 수 있는 방법?
import sys
import logging
sys.path.append('../')
from time import time
from config import MONGO_DB_HOST, MONGO_DB_PORT, APP_NAME
from api import mongo_db_client, redis_client

import hashlib
from aiohttp import web

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

    if not db_data or not (data['id'] == db_data['id'] and data['pw'] == db_data['pw']):
        return web.Response(status=401)
    else:
        if redis_client.get(req_data["id"]):
            logging.info(f"'{req_data['id']}' already logged in")

        redis_client.set(req_data["id"], time(), 24 * 3600)
        return web.Response(status=200)

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
    redis_client.delete(req_data["id"])
