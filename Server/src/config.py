import os

from dotenv import load_dotenv

load_dotenv()


class AuthConfig:
    API_KEY = os.environ.get("API_KEY")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")
    ALGORITHM = "HS256"
    ISSUER = "pic18api"
    EXPIRE_MINUTES = int(os.environ.get("EXPIRE_MINUTES", 30))


class MongoConfig:
    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_DB = os.environ.get("MONGO_DB")
    MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")


class ServerConfig:
    auth: AuthConfig = AuthConfig()
    mongo: MongoConfig = MongoConfig()


server_config = ServerConfig()
