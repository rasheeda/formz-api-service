from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app, support_credentials=True)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

ma = Marshmallow(app)

jwt = JWTManager(app)

from routes import *

if __name__ == '__main__':
    app.run()
