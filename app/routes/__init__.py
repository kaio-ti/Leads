from flask.app import Flask
from app.routes.vacinacao_blueprint import bp_vacina

def init_app(app: Flask):
    app.register_blueprint(bp_vacina)
    