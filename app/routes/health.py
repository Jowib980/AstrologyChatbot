from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from app.utils.astrology import get_zodiac_positions, calculate_health_index

bp = Blueprint("health", __name__)

@bp.route('/health', methods=['POST'])
def health_index_api():
    data = request.get_json()

    dob = data.get("dob")        # Expected format: YYYY-MM-DD
    tob = data.get("tob")        # Expected format: HH:MM
    place = data.get("place")    # e.g., "Delhi, India"

    if not dob or not tob or not place:
        return jsonify({"error": "Missing dob, tob, or place"}), 400

    zodiac_positions = get_zodiac_positions(dob, tob, place)
    if not zodiac_positions:
        return jsonify({"error": "Could not calculate zodiac positions"}), 500

    health_score = calculate_health_index(zodiac_positions)

    response = {
        "health_index": health_score
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
