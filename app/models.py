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

