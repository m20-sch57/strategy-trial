from flask import Flask
from server.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.routes import all, logged_in, logged_out, admin

