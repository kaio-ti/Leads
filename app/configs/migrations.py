from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):

    from app.models.vacinacao_model import Vacinacao

    Migrate(app, app.db)
