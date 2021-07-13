import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from datetime import datetime

from flask import Blueprint
from flask_paginate import Pagination, get_page_args

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
mongo.init_app(app)


def create_app():

    from football_memories.administration.routes import administration
    from football_memories.authentication.routes import authentication
    from football_memories.errors.routes import errors
    from football_memories.memories.routes import memories
    from football_memories.tournaments.routes import tournaments
    app.register_blueprint(administration)
    app.register_blueprint(authentication)
    app.register_blueprint(errors)
    app.register_blueprint(memories)
    app.register_blueprint(tournaments)
    return app
