# app.py
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from app.utils.nakshatra import generate_nakshatra_prediction

bp = Blueprint("nakshatra", __name__)

@bp.route("/nakshatra", methods=["POST"])
def nakshatra_api():
    data = request.get_json(force=True)
    dob = data.get("dob")
    tob = data.get("tob")
    place = data.get("place")

    if not dob or not tob or not place:
        return jsonify({"error": "Missing dob, tob, or place"}), 400

    result = generate_nakshatra_prediction(dob, tob, place)
    return jsonify(result)
