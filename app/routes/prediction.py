from flask import Blueprint, request, jsonify
from app.utils.character_prediction import get_character_prediction

bp = Blueprint("character_prediction", __name__)

@bp.route('/predict_character', methods=['POST'])
def predict_character():
    data = request.get_json()
    name = data.get('name')
    dob = data.get('dob')           # format: YYYY-MM-DD
    tob = data.get('tob')           # format: HH:MM
    place = data.get('place')       # e.g., "Delhi"

    try:
        prediction = get_character_prediction(dob, tob, place)
        return jsonify({
            "name": name,
            "character_prediction": prediction
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
