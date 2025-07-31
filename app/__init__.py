from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()  # <== THIS is what was missing from top level

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    from app.routes.chatbot import bp as chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix="/api")

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api")

    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.routes.kundali import bp as kundali_bp
    app.register_blueprint(kundali_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app

# ✅ Make these available when importing from app
__all__ = ['db', 'bcrypt']
