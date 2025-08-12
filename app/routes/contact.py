from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from app.models import db, Contact  # adjust import path as needed

bp = Blueprint("contact", __name__)
CORS(bp)  # Enable CORS if needed

@bp.route("/contact", methods=["POST"])
def submit_contact():
    data = request.get_json()

    # Validate required fields
    required_fields = ["first_name", "last_name", "email"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "First name, last name, and email are required."}), 400

    try:
        contact = Contact(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            subject=data.get("subject"),
            message=data.get("message")
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify({"message": "Message sent successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
