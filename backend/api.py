from config import *
from pymongo import MongoClient
import redis

mongo_db_client = MongoClient(host=MONGO_DB_HOST, port=int(MONGO_DB_PORT))

redis_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0, max_connections=4)
redis_client = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT), db=0, connection_pool=redis_pool, password="changeme")
