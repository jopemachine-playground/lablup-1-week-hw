import sys
import logging
sys.path.append('../')
import socketio

from socketio import Namespace

class ChatNamespace(socketio.AsyncNamespace):
    def __init__(self, sio, namespace):
        super(Namespace, self).__init__(namespace)

    def on_connect(self, sid, env):
        logging.info(f'{ sid } [SOCKET][CONNECT]')

    def on_disconnect(self, sid):
        logging.info(f'{ sid } [SOCKET][DISCONNECT]')

    async def on_message(self, sid, chat_data):
        logging.info(f'{ sid } [SOCKET][MESSAGE] { chat_data }')
        await self.emit("message", data=chat_data, namespace=self.namespace)

