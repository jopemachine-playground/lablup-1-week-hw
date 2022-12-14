from config import MONGO_DB_PORT, MONGO_DB_HOST, REDIS_HOST, REDIS_PORT, \
    REDIS_PW
from pymongo import MongoClient
import redis

mongo_db_client = MongoClient(
    host=MONGO_DB_HOST,
    port=int(MONGO_DB_PORT),
)

redis_userlogin_pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    db=0,
    max_connections=4,
)

redis_userlogin_client = redis.Redis(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    db=0,
    connection_pool=redis_userlogin_pool,
    password=REDIS_PW,
    decode_responses=True,
)
