from flask import Flask
from flask_bootstrap import Bootstrap
from app.AppConfig import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
bootstrap = Bootstrap(app)