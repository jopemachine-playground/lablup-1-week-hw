import logging
import socketio
from aiohttp import web
from routes.users import signin, signup, signout, check_login_session_is_valid
from routes.chatting_room import ChatNamespace
import aiohttp_cors


def setup_route(app, cors):
    app.add_routes([
        web.post('/api/v1/signin', signin),
        web.post('/api/v1/signup', signup),
        web.get('/api/v1/signout', signout),
        web.get('/api/v1/ping', check_login_session_is_valid),
    ])

    for route in list(app.router.routes()):
        cors.add(route)


def setup_websocket_server(app):
    sio = socketio.AsyncServer(
        async_mode="aiohttp",
        logger=True,
        engineio_logger=True,
        cors_allowed_origins='*',
        namespaces='*',
    )

    sio.register_namespace(ChatNamespace(sio, '/ws-chatting'))
    sio.attach(app)


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
    setup_websocket_server(app)

    web.run_app(app)


if __name__ == '__main__':
    main()
