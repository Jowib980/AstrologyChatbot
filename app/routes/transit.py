# app/routes/transit.py
from flask import Blueprint, request, jsonify
from app.utils.transit import transit_interpretations
from app.utils.calculate_chart import calculate_chart
from app.utils.kundalichart import generate_kundli_image_jpg
from datetime import datetime
from app import db
from app.models import TransitReport

bp = Blueprint("transit", __name__)

# Helper function to get house from lagna & planet sign
def get_house_from_lagna(lagna_sign, planet_sign):
    zodiac_order = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    lagna_index = zodiac_order.index(lagna_sign)
    planet_index = zodiac_order.index(planet_sign)
    return (planet_index - lagna_index) % 12 + 1

@bp.route("/transit", methods=["POST"])
def transit_api():
    try:
        data = request.json
        name = data.get("name")
        dob = data.get("dob")
        tob = data.get("tob")
        place = data.get("place")
        user_id = data.get("user_id")

        if not all([name, dob, tob, place]):
            return jsonify({"error": "Missing required parameters"}), 400

        # Get current date & time
        now = datetime.utcnow()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        # 1. Get CURRENT planetary positions (transit)
        chart = calculate_chart(current_date, current_time, place)
        ascendant_sign = chart["ascendant_sign"]

        transit_results = []

        # Prepare Kundli data for transit chart image
        kundli_data = {
            "name": f"Transit Chart for {name}",
            "dob": current_date,
            "tob": current_time,
            "place": place,
            "Ascendant": {"rashi": ascendant_sign}
        }

        # 2. Loop through planets & compute houses dynamically
        for planet, details in chart["planets"].items():
            sign = details["sign"]
            house = get_house_from_lagna(ascendant_sign, sign)

            # Add to kundli image data
            kundli_data[planet] = {"rashi": sign}

            # Get interpretation text
            interp = transit_interpretations.get(planet, {}).get(house, "No interpretation available.")

            transit_results.append({
                "planet": planet,
                "sign": sign,
                "house": house,
                "interpretation": interp
            })

        # 3. Generate transit chart image
        chart_img_base64 = generate_kundli_image_jpg(kundli_data, chart_type="transit")

        # 4. Save data in DB
        report = TransitReport(
            user_id=user_id,
            name=name,
            place=place,
            ascendant=ascendant_sign,
            transit_date=current_date,
            transit_time=current_time,
            transits=transit_results,
            chart_image_base64=chart_img_base64
        )
        db.session.add(report)
        db.session.commit()

        # 5. Return JSON response
        return jsonify({
            "name": name,
            "ascendant": ascendant_sign,
            "transits": transit_results,
            "transit_chart_base64": chart_img_base64
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

