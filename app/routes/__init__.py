from flask.app import Flask
from app.routes.lead_blueprint import bp_leads

def init_app(app: Flask):
    app.register_blueprint(bp_leads)
    