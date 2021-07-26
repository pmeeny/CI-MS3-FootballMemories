import os
from flask import (Flask)
from flask_pymongo import PyMongo

# App variables for setup and mongodb connectivity
app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
mongo.init_app(app)


def create_app():
    """
    Create an app with the administration, administration, errors, memories,
    tournaments blueprint routes
    """
    # Import the routes
    from football_memories.administration.routes import administration
    from football_memories.authentication.routes import authentication
    from football_memories.errors.routes import errors
    from football_memories.memories.routes import memories
    from football_memories.tournaments.routes import tournaments
    # Register the routes with the app
    app.register_blueprint(administration)
    app.register_blueprint(administration)
    app.register_blueprint(errors)
    app.register_blueprint(memories)
    app.register_blueprint(tournaments)
    # Return the app
    return app
