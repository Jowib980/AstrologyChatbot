# app/routes/transit.py
from flask import Blueprint, request, jsonify
from app.utils.transit import transit_interpretations
from app.utils.calculate_chart import calculate_chart
from app.utils.kundalichart import generate_kundli_image_jpg
from datetime import datetime

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

        if not all([name, dob, tob, place]):
            return jsonify({"error": "Missing required parameters"}), 400

        # 1. Get CURRENT planetary positions (transit)
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        chart = calculate_chart(now.split(" ")[0], now.split(" ")[1], place)
        ascendant_sign = chart["ascendant_sign"]

        transit_results = []

        # Prepare Kundli data for transit chart image
        kundli_data = {
            "name": f"Transit Chart for {name}",
            "dob": now.split(" ")[0],
            "tob": now.split(" ")[1],
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

        # 4. Return JSON response
        return jsonify({
            "name": name,
            "ascendant": ascendant_sign,
            "transits": transit_results,
            "transit_chart_base64": chart_img_base64
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
