import socketio
from aiohttp import web
from socketio import Namespace

routes = web.RouteTableDef()

sio = socketio.AsyncServer(logger=True, engineio_logger=True)

# Room과 이 Namespace를 연동시켜야 좋을 거 같은데.
class ChatterNamespace(socketio.AsyncNamespace):
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

@routes.get('/api/v1/chattingRoom/chats')
async def fetch_chatting_room_chatlogs(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
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
