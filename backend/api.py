from config import *
from pymongo import MongoClient
import redis

mongo_db_client = MongoClient(host=MONGO_DB_HOST, port=int(MONGO_DB_PORT))

redis_userlogin_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0, max_connections=4)
redis_userlogin_client = redis.Redis(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    db=0,
    connection_pool=redis_userlogin_pool,
    password=REDIS_PW,
    decode_responses=True,
)

redis_chatting_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0, max_connections=4)
redis_chatting_client = redis.Redis(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    db=0,
    connection_pool=redis_chatting_pool,
    password=REDIS_PW,
    decode_responses=True,
)
