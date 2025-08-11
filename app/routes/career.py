# routes.py
from flask import request, jsonify, Blueprint
from app.utils.career import generate_career_details
from app import db
from app.models import CareerReport
import json

bp = Blueprint('career', __name__)

@bp.route('/career', methods=['POST'])
def career_api():
    data = request.get_json()

    name = data.get('name')
    dob = data.get('dob')
    tob = data.get('tob')
    place = data.get('place')
    gender = data.get('gender', '')
    user_id = data.get('user_id')

    # Validate required fields
    if not all([name, dob, tob, place, gender, user_id]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result = generate_career_details(
            name=name,
            dob=dob,
            tob=tob,
            place=place,
            gender=gender
        )

        report = CareerReport(
            user_id=user_id,
            name=name,
            dob=dob,
            tob=tob,
            place=place,
            gender=gender,
            result=json.dumps(result)
        )

        db.session.add(report)
        db.session.commit()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
