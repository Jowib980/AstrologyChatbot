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
