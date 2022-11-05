import logging
from aiohttp import web
from routes import *
import aiohttp_cors

def setup_route(app, cors):
    app.add_routes([
        # 유저 정보 관련 기능
        web.post('/api/v1/signin', signin),
        web.post('/api/v1/signup', signup),
        web.get('/api/v1/signout', signout),

        # 채팅룸 페이지 기능
        web.get('/api/v1/chattingRoom/chats', fetch_chatting_room_chatlogs),
        # web.put('/api/v1/chattingRoom/chat', put_new_chat_log),
    ])

    for route in list(app.router.routes()):
        cors.add(route)

def setup_middlewares(app):
    pass

def setup_websocket_server():
    sio = socketio.AsyncServer(
        async_mode="aiohttp",
        async_handlers=True,
    )

    sio.register_namespace(ChatterNamespace(sio, '/ws-chatting'))

def main():
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()

    cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    setup_route(app=app, cors=cors)
    setup_middlewares(app)

    setup_websocket_server()
    web.run_app(app)

if __name__ == '__main__':
    main()
