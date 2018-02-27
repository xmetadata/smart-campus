from datetime import timedelta

# SERVER
DEBUG = True
PORT = 5000
HOST = "127.0.0.1"

# JWT
SECRET_KEY = "SOME SECRET"
JWT_EXPIRATION_DELTA = timedelta(seconds=3600)

# MYSQL
DB_USER = 'root'
DB_PASS = 'Aa888888'
DB_NAME = 'smart-campus'
DB_ADDR = '106.14.174.55'

SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = "mysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=DB_USER,
                                                                                   DB_PASS=DB_PASS,
                                                                                   DB_ADDR=DB_ADDR,
                                                                                   DB_NAME=DB_NAME)
