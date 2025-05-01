from flask import Flask
from flask_bootstrap import Bootstrap
from flask_session import Session
import redis, os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'you-will-never-guess'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')

from app import routes
bootstrap = Bootstrap(app)
server_session = Session(app)