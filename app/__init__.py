from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.auth.routes import auth
    from app.assets.routes import assets
    from app.assets.api import api

    app.register_blueprint(auth)
    app.register_blueprint(assets)
    app.register_blueprint(api)

    return app
