from flask import Blueprint, request, jsonify
from app.utils.numerology import generate_numerology_report, calculate_radical_number
from app import db
from app.models import NumerologyReport, NumerologyNumber
import json

bp = Blueprint("numerology", __name__)

@bp.route('/numerology', methods=['POST'])
def get_numerology():
    data = request.get_json()
    name = data.get('name')
    dob = data.get('dob')  # format: YYYY-MM-DD
    user_id = data.get('user_id')

    if not name or not dob:
        return jsonify({"error": "Missing required fields: name or dob"}), 400

    try:
        day = int(dob.split("-")[2])
        radical_number = calculate_radical_number(day)

        # Generate full report with DB-driven numerology data
        full_report = generate_numerology_report(name, dob)

        # Fetch numerology attributes directly from DB for radical number
        radical_entry = NumerologyNumber.query.filter_by(number=radical_number).first()
        if radical_entry:
            numerology_attributes = {
                "favourable_sign": radical_entry.favourable_sign,
                "favourable_alphabets": radical_entry.favourable_alphabets,
                "gemstone": radical_entry.gemstone,
                "favourable_days": radical_entry.favourable_days,
                "favourable_number": radical_entry.favourable_number,
                "direction": radical_entry.direction,
                "auspicious_color": radical_entry.auspicious_color,
                "ruling_planet": radical_entry.ruling_planet,
                "god_goddess": radical_entry.god_goddess,
                "fast": radical_entry.fast,
                "favourable_dates": radical_entry.favourable_dates,
                "mantra": radical_entry.mantra,
                "personality": radical_entry.personality,
                "career": radical_entry.career,
                "dos": [dos.advice for dos in radical_entry.dos],
                "donts": [dont.advice for dont in radical_entry.donts],
                "compatibles": [comp.compatible_number for comp in radical_entry.compatibles],
            }
        else:
            numerology_attributes = {}

        full_report["numerology_attributes"] = numerology_attributes

        # Save report in DB
        report = NumerologyReport(
            user_id=user_id,
            name=name,
            dob=dob,
            radical_number=radical_number,
            destiny_number=full_report['destiny_number'],
            name_number=full_report['name_number'],
            radical_meaning=full_report.get('radical_meaning', ''),
            destiny_meaning=full_report.get('destiny_meaning', ''),
            name_meaning=full_report.get('name_meaning', ''),
            numerology_attributes=json.dumps(numerology_attributes), 
        )
        db.session.add(report)
        db.session.commit()

        print(full_report)

        return jsonify(full_report)

    except Exception as e:
        return jsonify({"error": str(e)}), 400
