"""
application.py
- creates a Flask app instance and registers the database
"""

from imp import reload
from flask import Flask
from flask_cors import CORS
import sys
sys.path.append(r'./recommendation/')
import init_db

def create_app(app_name='SURVEY_API'):
    app = Flask(app_name)
    app.config.from_object('recommendation.config.BaseConfig')

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    from recommendation.api import api
    app.register_blueprint(api, url_prefix="/api")

    reload(init_db)
    return app
