from flask import Flask
from app.AppConfig import Config
import routes

app = Flask(__name__)
app.config.from_object(Config)