from flask import Blueprint, request, jsonify
from app.models import User, db  # ✅ import db from models
from app import bcrypt           # ✅ bcrypt from app/__init__.py

bp = Blueprint("auth", __name__)

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
        password_hash=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    # Return user data in response (excluding password)
    user_data = {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
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
            "email": user.email
        })
    return jsonify({"error": "Invalid email or password"}), 401
