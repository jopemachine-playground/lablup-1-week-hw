from aiohttp import web
from routes import *

app = web.Application()

# 버전 1 REST_API
# Q1. url 체계가 REST하게 충분히 표현되었는지?
app.add_routes([
    # 채팅룸 페이지 기능
    web.get('/api/v1/chattingRoom', fetch_chatting_room_info),
    web.get('/api/v1/chattingRoom/chats', fetch_chatting_room_chatlogs),
    web.put('/api/v1/chattingRoom/chat', put_new_chat_log),

    # 채팅룸 셀렉터 페이지 기능
    web.get('/api/v1/chattingRooms', fetch_chatting_rooms),
    web.put('/api/v1/chattingRooms', create_new_chatting_room),
])

if __name__ == '__main__':
    web.run_app(app)
