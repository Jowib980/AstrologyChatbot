from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from app.utils.match_horoscope import get_moon_rashi_nakshatra
from app.utils.match_kundali import match_all_kootas

bp = Blueprint("match_horoscope", __name__)

@bp.route("/match_horoscope", methods=["POST"])
def match_horoscope():
    data = request.get_json()
    
    user = {
        "name": data["user"]["name"],
        "dob": data["user"]["dob"],
        "tob": data["user"]["tob"],
        "place": data["user"]["place"]
    }
    partner = {
        "name": data["partner"]["name"],
        "dob": data["partner"]["dob"],
        "tob": data["partner"]["tob"],
        "place": data["partner"]["place"]
    }

    try:
        user_moon = get_moon_rashi_nakshatra(user["dob"], user["tob"], user["place"])
        partner_moon = get_moon_rashi_nakshatra(partner["dob"], partner["tob"], partner["place"])
        result = match_all_kootas(user_moon, partner_moon)

        return jsonify({
            "status": "success",
            "boy": user_moon,
            "girl": partner_moon,
            "guna_matching": result
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
