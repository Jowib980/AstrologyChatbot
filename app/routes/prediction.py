from flask import Blueprint, request, jsonify
from app.utils.character_prediction import get_character_prediction
from app.models import CharacterPrediction
from app import db
import json

bp = Blueprint("character_prediction", __name__)

@bp.route('/predict_character', methods=['POST'])
def predict_character():
    data = request.get_json()
    name = data.get('name')
    dob = data.get('dob')
    tob = data.get('tob')
    place = data.get('place')
    user_id = data.get('user_id')

    try:
        prediction = get_character_prediction(dob, tob, place)

        new_prediction = CharacterPrediction(
            user_id=user_id,
            name=name,
            dob=dob,
            tob=tob,
            place=place,
            prediction=json.dumps(prediction)
        )
        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({
            "name": name,
            **prediction
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
