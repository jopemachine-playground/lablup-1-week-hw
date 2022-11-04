from dotenv import load_dotenv, dotenv_values
load_dotenv()

MONGO_DB_HOST = dotenv_values(".env")["MONGO_DB_HOST"]
MONGO_DB_PORT = dotenv_values(".env")["MONGO_DB_PORT"]
REDIS_HOST = dotenv_values(".env")["REDIS_HOST"]
REDIS_PORT = dotenv_values(".env")["REDIS_PORT"]

APP_NAME = "chatting_app_backend"
