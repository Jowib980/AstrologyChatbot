from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from app.utils.astrology import get_zodiac_positions, calculate_health_index
from app import db
from app.models import HealthReport

bp = Blueprint("health", __name__)

@bp.route('/health', methods=['POST'])
def health_index_api():
    data = request.get_json()

    dob = data.get("dob")
    tob = data.get("tob")
    place = data.get("place")
    user_id = data.get("user_id")  # optional

    if not dob or not tob or not place:
        return jsonify({"error": "Missing dob, tob, or place"}), 400

    zodiac_positions = get_zodiac_positions(dob, tob, place)
    if not zodiac_positions:
        return jsonify({"error": "Could not calculate zodiac positions"}), 500

    health_score = calculate_health_index(zodiac_positions)

    # Save to database
    try:
        report = HealthReport(
            user_id=user_id,
            dob=dob,
            tob=tob, 
            place=place,
            health_index=health_score
        )
        db.session.add(report)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": f"Failed to save report: {str(e)}"}), 500

    return jsonify({"health_index": health_score}), 200
