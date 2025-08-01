from flask import Blueprint, request, jsonify
from app.utils.numerology import generate_numerology_report, calculate_radical_number, numerology_data

bp = Blueprint("numerology", __name__)

@bp.route('/numerology', methods=['POST'])
def get_numerology():
    data = request.get_json()
    name = data.get('name')
    dob = data.get('dob')  # format: YYYY-MM-DD

    try:
        day = int(dob.split("-")[2])
        radical_number = calculate_radical_number(day)
        numerology_attributes = numerology_data.get(radical_number, {})

        full_report = generate_numerology_report(name, dob)
        full_report["numerology_attributes"] = numerology_attributes

        return jsonify(full_report)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
