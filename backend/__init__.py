import logging
from aiohttp import web
from routes import *

def setup_route(app):
    app.add_routes([
        # 유저 정보 생성 등
        web.post('/api/v1/signin', signin),
        web.post('/api/v1/signup', signup),
        web.get('/api/v1/signout', signout),

        # 채팅룸 페이지 기능
        web.get('/api/v1/chattingRoom/chats', fetch_chatting_room_chatlogs),
        web.put('/api/v1/chattingRoom/chat', put_new_chat_log),
    ])

def setup_websocket_server():
    sio = socketio.AsyncServer(
        async_mode="aiohttp",
        async_handlers=True,
    )

    sio.register_namespace(ChatterNamespace(sio, '/chat'))

def main():
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    setup_route(app)
    setup_websocket_server()
    web.run_app(app)

if __name__ == '__main__':
    main()
