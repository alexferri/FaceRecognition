'''
 Author: Alexandre Ferri
 Created on Mon Dec 09 2019
'''

import os

from flask import Flask
from flask_cors import CORS

from .extentions import db

from .capture import bp_capture
from .training import bp_training
from .facialrecognition import bp_recognition

def create_app(config_file='config.py'):
    app = Flask(__name__)
    CORS(app)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.register_blueprint(bp_capture)
    app.register_blueprint(bp_training)
    app.register_blueprint(bp_recognition)

    return app