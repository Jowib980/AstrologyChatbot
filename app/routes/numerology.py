from flask import Blueprint, request, jsonify
from app.utils.numerology import generate_numerology_report, calculate_radical_number, numerology_data
from app import db
from app.models import NumerologyReport
import json

bp = Blueprint("numerology", __name__)

@bp.route('/numerology', methods=['POST'])
def get_numerology():
    data = request.get_json()
    name = data.get('name')
    dob = data.get('dob')  # format: YYYY-MM-DD
    user_id = data.get('user_id')

    try:
        day = int(dob.split("-")[2])
        radical_number = calculate_radical_number(day)
        
        numerology_attributes = numerology_data.get(radical_number, {})
        full_report = generate_numerology_report(name, dob)
        full_report["numerology_attributes"] = numerology_attributes

        report = NumerologyReport(
            user_id=user_id,
            name=name,
            dob=dob,
            radical_number=radical_number,
            destiny_number=full_report['destiny_number'],
            name_number=full_report['name_number'],
            radical_meaning=full_report['radical_meaning'],
            destiny_meaning=full_report['destiny_meaning'],
            name_meaning=full_report['name_meaning'],
            numerology_attributes=json.dumps(numerology_attributes),
        )
        db.session.add(report)
        db.session.commit()

        return jsonify(full_report)

    except Exception as e:
        return jsonify({"error": str(e)}), 400
