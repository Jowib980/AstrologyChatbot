from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
import json

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
    career = db.Column(db.Text)

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

# Nakshatra trait data table

class Nakshatra(db.Model):
    __tablename__ = 'nakshatras'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    keywords = db.Column(db.Text)  # JSON string

    # Relationship to padas
    padas = db.relationship('Pada', backref='nakshatra', cascade='all, delete-orphan')

    def get_keywords(self):
        if self.keywords:
            return json.loads(self.keywords)
        return []

class Pada(db.Model):
    __tablename__ = 'padas'
    id = db.Column(db.Integer, primary_key=True)
    nakshatra_id = db.Column(db.Integer, db.ForeignKey('nakshatras.id'), nullable=False)
    pada_number = db.Column(db.Integer, nullable=False)
    personality = db.Column(db.Text)
    strengths = db.Column(db.Text)  # JSON string
    weaknesses = db.Column(db.Text)  # JSON string
    career = db.Column(db.Text)  # JSON string
    emotional_traits = db.Column(db.Text)
    ideal_partner = db.Column(db.Text)

    def get_strengths(self):
        return json.loads(self.strengths) if self.strengths else []

    def get_weaknesses(self):
        return json.loads(self.weaknesses) if self.weaknesses else []

    def get_career(self):
        return json.loads(self.career) if self.career else []

class AscendantSign(db.Model):
    __tablename__ = "ascendant_sign"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    element = db.Column(db.String(20))
    ruling_planet = db.Column(db.String(50))

    traits = db.relationship('AscendantTrait', backref='ascendant_sign', lazy=True)

class AscendantTrait(db.Model):
    __tablename__ = "ascendant_trait"
    id = db.Column(db.Integer, primary_key=True)
    ascendant_sign_id = db.Column(db.Integer, db.ForeignKey('ascendant_sign.id'), nullable=False)
    trait_type = db.Column(db.String(20))  # e.g., health, personality, appearance
    description = db.Column(db.Text)


class CareerMapping(db.Model):
    __tablename__ = "career_mappings"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    sign_or_house = db.Column(db.String(20), nullable=False)
    career_description = db.Column(db.Text, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('category', 'sign_or_house', name='uix_category_sign_or_house'),
    )


class CharacterSign(db.Model):
    __tablename__ = "character_sign"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    ruled_by = db.Column(db.String(50))
    traits = db.relationship("CharacterTrait", backref="character_sign", lazy=True)

class CharacterTrait(db.Model):
    __tablename__ = "character_trait"
    id = db.Column(db.Integer, primary_key=True)
    character_sign_id = db.Column(db.Integer, db.ForeignKey("character_sign.id"), nullable=False)
    trait_type = db.Column(db.String(50))  # e.g. core, strengths, challenges, happiness, fulfillment, lifestyle
    description = db.Column(db.Text)

class NumerologyNumber(db.Model):
    __tablename__ = 'numerology_numbers'
    number = db.Column(db.Integer, primary_key=True)
    favourable_sign = db.Column(db.String(50))
    favourable_alphabets = db.Column(db.String(100))
    gemstone = db.Column(db.String(50))
    favourable_days = db.Column(db.String(100))
    favourable_number = db.Column(db.String(100))
    direction = db.Column(db.String(50))
    auspicious_color = db.Column(db.String(100))
    ruling_planet = db.Column(db.String(50))
    god_goddess = db.Column(db.String(100))
    fast = db.Column(db.String(50))
    favourable_dates = db.Column(db.String(100))
    mantra = db.Column(db.String(200))
    personality = db.Column(db.Text)
    career = db.Column(db.Text)

    # relationships
    dos = db.relationship('NumerologyDos', backref='number', cascade='all, delete-orphan')
    donts = db.relationship('NumerologyDonts', backref='number', cascade='all, delete-orphan')
    compatibles = db.relationship('NumerologyCompatible', backref='number', cascade='all, delete-orphan')


class NumerologyDos(db.Model):
    __tablename__ = 'numerology_dos'
    id = db.Column(db.Integer, primary_key=True)
    number_id = db.Column(db.Integer, db.ForeignKey('numerology_numbers.number'))
    advice = db.Column(db.String(255))


class NumerologyDonts(db.Model):
    __tablename__ = 'numerology_donts'
    id = db.Column(db.Integer, primary_key=True)
    number_id = db.Column(db.Integer, db.ForeignKey('numerology_numbers.number'))
    advice = db.Column(db.String(255))


class NumerologyCompatible(db.Model):
    __tablename__ = 'numerology_compatibles'
    id = db.Column(db.Integer, primary_key=True)
    number_id = db.Column(db.Integer, db.ForeignKey('numerology_numbers.number'))
    compatible_number = db.Column(db.Integer)


class TransitInterpretation(db.Model):
    __tablename__ = 'transit_interpretations'
    id = db.Column(db.Integer, primary_key=True)
    planet = db.Column(db.String(50), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    interpretation = db.Column(db.Text, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('planet', 'house_number', name='unique_planet_house'),
    )

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(100), nullable=True)  # e.g. 'birth-kundali-card'
    title = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    route = db.Column(db.String(255), nullable=False)
    link = db.Column(db.Boolean, default=False)  # For items like 'Match Horoscope'
    fields = db.Column(db.Text, nullable=True)  # Store as comma-separated string

    __table_args__ = (
        db.UniqueConstraint('title', name='unique_service_title'),
    )


class Rashis(db.Model):
    __tablename__ = 'rashis'
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(100), nullable=True)
    icon = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    route = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('title', name='unique_rashis_title'),
    )