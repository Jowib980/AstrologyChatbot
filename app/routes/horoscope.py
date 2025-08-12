from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from app.utils.match_horoscope import get_moon_rashi_nakshatra, rashis, nakshatras
from app.utils.match_kundali import match_all_kootas
from app import db
from app.models import HoroscopeMatch
import json
import ast

bp = Blueprint("match_horoscope", __name__)

@bp.route("/match_horoscope", methods=["POST"])
def match_horoscope():
    data = request.get_json()

    user = data["user"]
    partner = data["partner"]

    try:
        user_moon = get_moon_rashi_nakshatra(user["dob"], user["tob"], user["place"])
        partner_moon = get_moon_rashi_nakshatra(partner["dob"], partner["tob"], partner["place"])

        boy = {
            "rashi": rashis.index(user_moon["rashi"]) + 1,
            "nakshatra": nakshatras.index(user_moon["nakshatra"])
        }
        girl = {
            "rashi": rashis.index(partner_moon["rashi"]) + 1,
            "nakshatra": nakshatras.index(partner_moon["nakshatra"])
        }

        result = match_all_kootas(boy, girl)

        # ✅ Save only if user_id is present
        if "user_id" in user and user["user_id"]:
            match = HoroscopeMatch(
                user_id=user['user_id'],
                user_name=user["name"],
                user_dob=user["dob"],
                user_tob=user["tob"],
                user_place=user["place"],
                user_gender=user["gender"],
                user_rashi=user_moon["rashi"],
                user_nakshatra=user_moon["nakshatra"],

                partner_name=partner["name"],
                partner_dob=partner["dob"],
                partner_tob=partner["tob"],
                partner_place=partner["place"],
                partner_gender=partner["gender"],
                partner_rashi=partner_moon["rashi"],
                partner_nakshatra=partner_moon["nakshatra"],

                total_guna=result["total_score"],
                matching_result=str(result)
            )
            db.session.add(match)
            db.session.commit()

        return jsonify({
            "status": "success",
            "match_id": match.id,
            "boy": user_moon,
            "girl": partner_moon,
            "guna_matching": result
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@bp.route("/get_match/<int:match_id>", methods=["GET"])
def get_match(match_id):
    
    match = HoroscopeMatch.query.get(match_id)
    if not match:
        return jsonify({"status": "error", "message": "Match not found"}), 404

    # Convert Python dict string to Python dict
    matching_result_dict = None
    if match.matching_result:
        try:
            matching_result_dict = ast.literal_eval(match.matching_result)  # safely parse Python dict string
        except Exception as e:
            print("Error parsing matching_result:", e)

    return jsonify({
        "status": "success",
        "data": {
            "id": match.id,
            "user_name": match.user_name,
            "user_dob": match.user_dob,
            "partner_name": match.partner_name,
            "total_guna": match.total_guna,
            "matching_result": matching_result_dict  # send as actual JSON object
        }
    })
