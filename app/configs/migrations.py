from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):

    from app.models.lead_model import Leads

    Migrate(app, app.db)
