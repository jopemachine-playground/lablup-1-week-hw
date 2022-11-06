import sys
import logging
sys.path.append('../')
from api import redis_userlogin_client, redis_chatting_client
from utils import is_valid_user

import socketio
from aiohttp import web
from socketio import Namespace
import json

routes = web.RouteTableDef()

class ChatNamespace(socketio.AsyncNamespace):
  def __init__(self, sio, namespace, *args, **kwargs):
    super(Namespace, self).__init__(namespace)

    def on_connect(self, sid, env):
        logging.info(f'{ sid } [SOCKET][CONNECT]')

    def on_disconnect(self, sid):
        logging.info(f'{ sid } [SOCKET][DISCONNECT]')

    def on_message(self, sid, chat):
        logging.info(f'{ sid } [SOCKET][MESSAGE] { chat }')

        chat_json = json.loads(redis_chatting_client.get('data').decode('utf-8'))

        if not chat_json['chats']:
            chat_json['chats'] = []

        chat_json['chats'] += {
            'message': chat.message,
            'created_at': chat.created_at,
            'created_by': chat.created_by,
        }

        self.emit("chat", json.dumps(chat_json, ensure_ascii=False).encode('utf-8'))

@routes.post('/api/v1/chattingRoom/chats')
async def fetch_chatting_room_chatlogs(request):
    try:
        req_data = await request.json()
    except Exception as e:
        logging.error(e)
        return web.Response(status=400, reason=e.__cause__)

    if not is_valid_user(user_id=req_data["id"], session_id=req_data["session-id"]):
        return web.Response(status=401)

    if redis_chatting_client.get('data'):
        chat_data = redis_chatting_client.get('data').decode('utf-8')
        return web.Response(status=200, text=chat_data)
    else:
        return web.Response(status=200, text=json.dumps({'chats': []}, ensure_ascii=False))

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
