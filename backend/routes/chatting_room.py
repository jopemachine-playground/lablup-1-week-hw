import sys
import logging
sys.path.append('../')
from api import redis_userlogin_client, redis_chatting_client

import socketio
from aiohttp import web
from socketio import Namespace
from urllib.parse import urlsplit, parse_qsl
import json

routes = web.RouteTableDef()

sio = socketio.AsyncServer(logger=True, engineio_logger=True)

class ChatterNamespace(socketio.AsyncNamespace):
  def __init__(self, sio, namespace, *args, **kwargs):
    super(Namespace, self).__init__(namespace)

    self.sio = sio
    self.logger = sio.logger

    def on_connect(self, sid, env):
        params = dict(parse_qsl(urlsplit(env["QUERY_STRING"]).path))
        self.sio.logger.info(f'{ sid } [SOCKET][CONNECT]')
        self.sio.logger.info(f'{ sid } [SOCKET][CONNECT][PARAMS] { params }')

        chat_data = redis_chatting_client.get('chat').decode('utf-8')
        self.emit("init_chatting_room", chat_data)

    def on_message(self, sid, data):
        self.sio.logger.info(f'{ sid } [SOCKET][MESSAGE] { data }')

        chat_json = json.loads(redis_chatting_client.get('chat').decode('utf-8'))
        chat_json['chat'] += {
            'message': data.message,
            'created_at': data.created_at,
            'created_by': data.created_by,
        }

        self.emit("receive_chat", json.dumps(chat_json, ensure_ascii=False).encode('utf-8'))

    def on_disconnect(self, sid):
        self.sio.logger.info(f'{ sid } [SOCKET][DISCONNECT]')

@routes.get('/api/v1/chattingRoom/chats')
async def fetch_chatting_room_chatlogs(request):
    # chat_data = json.dumps(, ensure_ascii=False).encode('utf-8')
    json.loads()
    return web.Response(text=text)

@routes.put('/api/v1/chattingRoom/chat')
async def put_new_chat_log(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.text:
            await ws.send_str("Hello, {}".format(msg.data))
        elif msg.type == web.WSMsgType.binary:
            await ws.send_bytes(msg.data)
        elif msg.type == web.WSMsgType.close:
            break

    return ws
