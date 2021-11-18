from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):

    from app.models.salgado_model import SalgadoModel

    Migrate(app, app.db)
