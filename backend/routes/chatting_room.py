import sys
import logging
sys.path.append('../')
from api import redis_userlogin_client, redis_chatting_client
from utils import is_valid_user

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
        self.sio.logger.info(f'{ sid } [SOCKET][CONNECT]')

    def on_disconnect(self, sid):
        self.sio.logger.info(f'{ sid } [SOCKET][DISCONNECT]')

    def on_message(self, sid, data):
        self.sio.logger.info(f'{ sid } [SOCKET][MESSAGE] { data }')

        chat_json = json.loads(redis_chatting_client.get('chat').decode('utf-8'))
        chat_json['chat'] += {
            'message': data.message,
            'created_at': data.created_at,
            'created_by': data.created_by,
        }

        self.emit("chat", json.dumps(chat_json, ensure_ascii=False).encode('utf-8'))

@routes.get('/api/v1/chattingRoom/chats')
async def fetch_chatting_room_chatlogs(request):
    if not is_valid_user(user_id=req_data["id"], session_id=req_data["session-id"]):
        return web.Response(status=401)

    chat_data = redis_chatting_client.get('chat').decode('utf-8')
    return web.Response(text=chat_data)

# @routes.put('/api/v1/chattingRoom/chat')
# async def put_new_chat_log(request):
#     ws = web.WebSocketResponse()
#     await ws.prepare(request)

#     async for msg in ws:
#         if msg.type == web.WSMsgType.text:
#             await ws.send_str("Hello, {}".format(msg.data))
#         elif msg.type == web.WSMsgType.binary:
#             await ws.send_bytes(msg.data)
#         elif msg.type == web.WSMsgType.close:
#             break

#     return ws
