from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Kundali-related fields (nullable)
    dob = db.Column(db.Date, nullable=True)
    time_of_birth = db.Column(db.String(20), nullable=True)
    place_of_birth = db.Column(db.String(150), nullable=True)
    gender = db.Column(db.String(20), nullable=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.Text, nullable=True)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HoroscopeMatch(db.Model):
    __tablename__ = 'horoscope_matches'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_dob = db.Column(db.Date, nullable=False)
    user_tob = db.Column(db.Time, nullable=False)
    user_place = db.Column(db.String(150), nullable=False)
    user_gender = db.Column(db.String(10), nullable=False)
    user_rashi = db.Column(db.String(50))
    user_nakshatra = db.Column(db.String(50))

    partner_name = db.Column(db.String(100), nullable=False)
    partner_dob = db.Column(db.Date, nullable=False)
    partner_tob = db.Column(db.Time, nullable=False)
    partner_place = db.Column(db.String(150), nullable=False)
    partner_gender = db.Column(db.String(10), nullable=False)
    partner_rashi = db.Column(db.String(50))
    partner_nakshatra = db.Column(db.String(50))

    total_guna = db.Column(db.Integer)
    matching_result = db.Column(db.Text)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship('User', backref=db.backref('horoscope_matches', lazy=True))

class AscendantReport(db.Model):
    __tablename__ = 'ascendant_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    name = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    tob = db.Column(db.String(10))
    place = db.Column(db.String(100))
    ascendant = db.Column(db.String(50))
    traits = db.Column(db.Text)  # JSON-encoded string of traits

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('ascendant_reports', lazy=True))

class CharacterPrediction(db.Model):
    __tablename__ = 'character_predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    tob = db.Column(db.Time, nullable=False)
    place = db.Column(db.String(100), nullable=False)
    prediction = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('character_predictions', lazy=True))

class Kundalis(db.Model):
    __tablename__ = 'kundalis'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    tob = db.Column(db.Time, nullable=False)
    place = db.Column(db.String(100), nullable=False)
    lagna_chart_path = db.Column(db.String(255), nullable=True)
    navamsa_chart_path = db.Column(db.String(255), nullable=True)

class NumerologyReport(db.Model):
    __tablename__ = 'numerology_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    name = db.Column(db.String(100))
    dob = db.Column(db.Date)

    radical_number = db.Column(db.Integer)
    destiny_number = db.Column(db.Integer)
    name_number = db.Column(db.Integer)

    radical_meaning = db.Column(db.Text)
    destiny_meaning = db.Column(db.Text)
    name_meaning = db.Column(db.Text)

    numerology_attributes = db.Column(db.Text)  # JSON-encoded string

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('numerology_reports', lazy=True))

class NakshatraReport(db.Model):
    __tablename__ = 'nakshatra_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    dob = db.Column(db.String(20))
    tob = db.Column(db.String(20))
    place = db.Column(db.String(100))
    nakshatra = db.Column(db.String(50))
    pada = db.Column(db.Integer)
    personality = db.Column(db.Text)
    
    strengths = db.Column(db.Text)
    weaknesses = db.Column(db.Text)
    ideal_partner = db.Column(db.Text)
    keywords = db.Column(db.Text)
    prediction = db.Column(db.Text)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

class HealthReport(db.Model):
    __tablename__ = 'health_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)  # Optional
    dob = db.Column(db.String(20), nullable=False)
    tob = db.Column(db.String(10), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    health_index = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LoveReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(20))
    tob = db.Column(db.String(10))
    place = db.Column(db.String(100))
    nakshatra = db.Column(db.String(50))
    pada = db.Column(db.String(10))
    love_prediction = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class GemstoneReport(db.Model):
    __tablename__ = 'gemstone_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50))
    name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(20))
    tob = db.Column(db.String(10))
    place = db.Column(db.String(255))

    ascendant = db.Column(db.String(20))
    moon_sign = db.Column(db.String(20))
    house_9_sign = db.Column(db.String(20))

    life_stone = db.Column(db.String(50))
    lucky_stone = db.Column(db.String(50))
    bhagya_stone = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=db.func.now())

class CareerReport(db.Model):
    __tablename__ = 'career_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50))
    name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(20))
    tob = db.Column(db.String(10))
    place = db.Column(db.String(255))
    result = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=db.func.now())


class KalsarpReport(db.Model):
    __tablename__ = 'kalsarp_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    tob = db.Column(db.String(10), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    ascendant = db.Column(db.String(50), nullable=True)
    moon_sign = db.Column(db.String(50), nullable=True)
    has_kalsarp_dosh = db.Column(db.Boolean, nullable=False)
    dosh_message = db.Column(db.Text, nullable=True)
    chart_base64 = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class MangalReport(db.Model):
    __tablename__ = 'mangal_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    tob = db.Column(db.String(20), nullable=False)
    place = db.Column(db.String(150), nullable=False)
    ascendant = db.Column(db.String(50), nullable=False)
    moon_sign = db.Column(db.String(50), nullable=False)
    mangal_present = db.Column(db.Boolean, nullable=False)
    severity = db.Column(db.String(50), nullable=True)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TransitReport(db.Model):
    __tablename__ = 'transit_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Link to users table
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(150), nullable=False)
    ascendant = db.Column(db.String(50), nullable=False)
    transit_date = db.Column(db.String(20), nullable=False)
    transit_time = db.Column(db.String(20), nullable=False)
    transits = db.Column(db.JSON, nullable=False)  # Stores planets, signs, houses, interpretations
    chart_image_base64 = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)