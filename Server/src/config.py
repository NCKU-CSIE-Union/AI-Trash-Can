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


class MailConfig:
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_FROM = os.environ.get("MAIL_FROM")
    MAIL_PORT = int(os.environ.get("MAIL_PORT"))
    MAIL_STARTTLS = bool(os.environ.get("MAIL_STARTTLS"))
    MAIL_SSL_TLS = bool(os.environ.get("MAIL_SSL_TLS"))
    MAIL_USE_CREDENTIALS = bool(os.environ.get("MAIL_USE_CREDENTIALS"))
    MAIL_VALIDATE_CERTS = bool(os.environ.get("MAIL_VALIDATE_CERTS"))
    MAIL_TEMPLATE_PATH = os.environ.get("MAIL_TEMPLATE_PATH")
    MAIL_TIMEOUT = int(os.environ.get("MAIL_TIMEOUT"))


class MongoConfig:
    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_DB = os.environ.get("MONGO_DB")
    MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")


class ServerConfig:
    auth: AuthConfig = AuthConfig()
    mail: MailConfig = MailConfig()
    mongo: MongoConfig = MongoConfig()


server_config = ServerConfig()
