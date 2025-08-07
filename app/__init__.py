from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from app.config import Config
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()  # <== THIS is what was missing from top level

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    from app.routes.chatbot import bp as chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix="/api")

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api")

    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.routes.kundali import bp as kundali_bp
    app.register_blueprint(kundali_bp, url_prefix="/api")

    from app.routes.horoscope import bp as horoscope_bp
    app.register_blueprint(horoscope_bp, url_prefix="/api")

    from app.routes.prediction import bp as prediction_bp
    app.register_blueprint(prediction_bp, url_prefix="/api")

    from app.routes.numerology import bp as numerology_bp
    app.register_blueprint(numerology_bp, url_prefix="/api")

    from app.routes.nakshatra import bp as nakshatra_bp
    app.register_blueprint(nakshatra_bp, url_prefix="/api")

    from app.routes.health import bp as health_bp
    app.register_blueprint(health_bp, url_prefix="/api")

    from app.routes.love import bp as love_bp
    app.register_blueprint(love_bp, url_prefix="/api")

    from app.routes.gemstone import bp as gemstone_bp
    app.register_blueprint(gemstone_bp, url_prefix="/api")

    from app.routes.career import bp as career_bp
    app.register_blueprint(career_bp, url_prefix="/api")

    from app.routes.kalsarp import bp as kalsarp_bp
    app.register_blueprint(kalsarp_bp, url_prefix="/api")

    from app.routes.mangal import bp as mangal_bp
    app.register_blueprint(mangal_bp, url_prefix="/api")

    from app.routes.ascendant import bp as ascendant_bp
    app.register_blueprint(ascendant_bp, url_prefix="/api")

    from app.routes.transit import bp as transit_bp
    app.register_blueprint(transit_bp, url_prefix="/api")

    from app.routes.contact import bp as contact_bp
    app.register_blueprint(contact_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app

# ✅ Make these available when importing from app
__all__ = ['db', 'bcrypt']
