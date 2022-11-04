import logging
from aiohttp import web
from routes import *

def setup_route(app):
    # 버전 1 REST_API
    # Q1. url 체계가 REST하게 충분히 표현되었는지?
    app.add_routes([
        # 유저 정보 생성 등
        web.post('/api/v1/signin', signin),
        web.post('/api/v1/signup', signup),
        web.get('/api/v1/signout', signout),

        # 채팅룸 페이지 기능
        web.get('/api/v1/chattingRoom', fetch_chatting_room_info),
        web.get('/api/v1/chattingRoom/chats', fetch_chatting_room_chatlogs),
        web.put('/api/v1/chattingRoom/chat', put_new_chat_log),
    ])

def main():
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    setup_route(app)
    web.run_app(app)

if __name__ == '__main__':
    main()
