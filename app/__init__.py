from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from config import Config

app = Flask(__name__)

# Initialize config from config.py
app.config.from_object(Config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize flask-restx
api = Api(app)

from app import routes