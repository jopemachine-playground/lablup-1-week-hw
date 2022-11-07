import sys
import logging
sys.path.append('../')
from api import redis_chatting_client
from utils import is_valid_user

import socketio
import aiohttp
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

@routes.get('/api/v1/chattingRoom/chats')
def fetch_chatting_room_chatlogs(request):
    user_id = request.cookies.get('user_id')
    session_id = request.cookies.get('session_id')

    if not is_valid_user(user_id=user_id, session_id=session_id):
        return web.Response(status=401)

    if redis_chatting_client.get('data'):
        chat_data = redis_chatting_client.get('data').decode('utf-8')
        return web.Response(status=200, text=chat_data)
    else:
        return web.Response(status=200, text=json.dumps({'chats': []}, ensure_ascii=False))

