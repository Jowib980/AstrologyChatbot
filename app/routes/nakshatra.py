# app.py
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from app.utils.nakshatra import generate_nakshatra_prediction
from app import db
from app.models import NakshatraReport
import json


bp = Blueprint("nakshatra", __name__)

@bp.route("/nakshatra", methods=["POST"])
def nakshatra_api():
    data = request.get_json(force=True)
    dob = data.get("dob")
    tob = data.get("tob")
    place = data.get("place")
    user_id = data.get("user_id")

    if not dob or not tob or not place:
        return jsonify({"error": "Missing dob, tob, or place"}), 400

    result = generate_nakshatra_prediction(dob, tob, place)

    try:
        report = NakshatraReport(
            user_id=user_id,
            dob=dob,
            tob=tob,
            place=place,
            nakshatra=result.get("nakshatra"),
            pada=result.get("pada"),
            personality=result.get("personality"),
            strengths=json.dumps(result.get("strengths")),
            weaknesses=json.dumps(result.get("weaknesses")),
            ideal_partner=result.get("ideal_partner"),
            keywords=json.dumps(result.get("keywords")),
            prediction=result.get("prediction")
        )

        db.session.add(report)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": f"Failed to save report: {str(e)}"}), 500

    return jsonify(result)
