from datetime import timedelta

#jwt config
JWT_AUTH_URL_RULE      = '/auth'
JWT_AUTH_USERNAME_KEY  = 'username'
JWT_AUTH_PASSWORD_KEY  = 'password'
JWT_LEEWAY             = timedelta(seconds=10)
JWT_EXPIRATION_DELTA   = timedelta(seconds=300)
JWT_NOT_BEFORE_DELTA   = timedelta(seconds=0)

# SERVER
DEBUG = True
PORT = 5000
HOST = "0.0.0.0"

# JWT
SECRET_KEY = "smart-campus is supported by xmetadata"
JWT_EXPIRATION_DELTA = timedelta(seconds=3600)

# MYSQL
DB_USER = 'root'
DB_PASS = 'Aa888888'
DB_NAME = 'SmartCampus'
DB_ADDR = '192.168.31.89'
DB_PORT = 16868

SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = "mysql://{DB_USER}:{DB_PASS}@{DB_ADDR}:{DB_PORT}/{DB_NAME}".format(DB_USER=DB_USER,
                                                                                   DB_PASS=DB_PASS,
                                                                                   DB_ADDR=DB_ADDR,
                                                                                   DB_PORT=DB_PORT,
                                                                                   DB_NAME=DB_NAME)
