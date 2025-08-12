from flask import Blueprint, request, jsonify
from app.models import User, db  # ✅ import db from models
from app import bcrypt           # ✅ bcrypt from app/__init__.py
from datetime import date, datetime

bp = Blueprint("auth", __name__)


def format_date(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 409

    # Hash password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Create and save new user
    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=hashed_password,
        dob=data['dob'],
        time_of_birth=data['tob'],
        place_of_birth=data['place'],
        gender=data['gender']
    )
    db.session.add(new_user)
    db.session.commit()

    # Return user data in response (excluding password)
    user_data = {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "dob": format_date(new_user.dob),
        "tob": new_user.time_of_birth,
        "place": new_user.place_of_birth,
        "gender": new_user.gender
    }

    return jsonify({
        "message": "User registered successfully!",
        "user": user_data
    }), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "dob": format_date(user.dob),
            "tob": user.time_of_birth,
            "place": user.place_of_birth,
            "gender": user.gender
        })
    return jsonify({"error": "Invalid email or password"}), 401
