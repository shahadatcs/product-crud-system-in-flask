from flask import Flask
from flask_pymongo import PyMongo
from app.database import initialize_db


def create_app():
    app = Flask(__name__)

    # secret_key = os.urandom(24)
    # app.config["SECRET_KEY"] = secret_key

    initialize_db(app)

    from app.auth.routes import auth_bp
    # from app.dashboard.routes import dashboard_bp
    # from app.admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    # app.register_blueprint(dashboard_bp)
    # app.register_blueprint(admin_bp)

    return app
