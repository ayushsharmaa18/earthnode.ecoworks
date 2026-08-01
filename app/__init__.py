import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy.exc import SQLAlchemyError

from config import config
try:
    import razorpay
except ImportError:
    razorpay = None

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "admin.login"
login_manager.login_message = "Please log in to access the admin panel."
login_manager.login_message_category = "info"


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    key_id = app.config.get("RAZORPAY_KEY_ID")
    key_secret = app.config.get("RAZORPAY_KEY_SECRET")

    if razorpay and key_id and key_secret:
        app.razorpay_client = razorpay.Client(
            auth=(key_id, key_secret)
        )
    else:
        app.razorpay_client = None

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import AdminUser

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(AdminUser, int(user_id))
        except (ValueError, TypeError, SQLAlchemyError):
            return None

    from app.routes.main import main_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template("404.html"), 404

    return app
