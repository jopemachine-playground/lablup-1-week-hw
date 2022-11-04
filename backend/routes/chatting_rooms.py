import socketio
from aiohttp import web

class ChattingRoomSelector(socketio.AsyncNamespace):
  def __init__(self, sio, namespace, *args, **kwargs):
    super(Namespace, self).__init__(namespace)

    self.sio = sio
    self.logger = sio.logger

    def on_connect(self, sid, env):
        params = dict(parse_qsl(urlsplit(env["QUERY_STRING"]).path))
        self.sio.logger.info(f'{ sid } [SOCKET][CONNECT]')
        self.sio.logger.info(f'{ sid } [SOCKET][CONNECT][PARAMS] { params }')

    def on_message(self, sid, data):
        self.sio.logger.info(f'{ sid } [SOCKET][MESSAGE] { data }')
        self.emit("receive_message", data)

    def on_disconnect(self, sid):
        self.sio.logger.info(f'{ sid } [SOCKET][DISCONNECT]')

async def fetch_chatting_rooms(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def create_new_chatting_room(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)
