from flask import Flask
from environs import Env
from app import routes
from app.configs import database, migrations


def create_app():

    app = Flask(__name__)

    env = Env()
    env.read_env()

    app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    database.init_app(app)
    migrations.init_app(app)

    routes.init_app(app)
    return app
