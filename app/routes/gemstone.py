from flask import Flask, request, jsonify, Blueprint
from datetime import datetime
from app.utils.numerology import generate_numerology_report
from app import db
from app.models import GemstoneReport

bp = Blueprint("gemstone", __name__)

# Planet to gemstone mapping
gemstone_data = {
    "Sun": {"gem": "Ruby (Manik)", "weight": "3 Carats", "metal": "Gold", "finger": "Ring finger",
            "mantra": "Om hram hrim hraum sah suryaya namah"},
    "Moon": {"gem": "Pearl (Moti)", "weight": "2 Carats", "metal": "Silver", "finger": "Little finger",
             "mantra": "Om shram shrim shraum sah chandraya namah"},
    "Mars": {"gem": "Red Coral (Moonga)", "weight": "3 Carats", "metal": "Gold", "finger": "Ring finger",
             "mantra": "Om kram krim kraum sah bhaumaya namah"},
    "Mercury": {"gem": "Emerald (Panna)", "weight": "1.5 Carats", "metal": "Gold", "finger": "Little finger",
                "mantra": "Om bram brim braum sah budhaya namah"},
    "Jupiter": {"gem": "Yellow Sapphire (Pukhraj)", "weight": "2 Carats", "metal": "Gold", "finger": "Index finger",
                "mantra": "Om gram grim graum sah gurave namah"},
    "Venus": {"gem": "Diamond (Heera)", "weight": "1 Carat", "metal": "Gold or Silver", "finger": "Middle finger",
              "mantra": "Om dram drim draum sah shukraya namah"},
    "Saturn": {"gem": "Blue Sapphire (Neelam)", "weight": "2 Carats", "metal": "Gold", "finger": "Middle finger",
               "mantra": "Om pram prim praum sah shanaisharaya namah"},
    "Rahu": {"gem": "Hessonite (Gomed)", "weight": "2 Carats", "metal": "Silver", "finger": "Middle finger",
             "mantra": "Om bhram bhrim bhraum sah rahave namah"},
    "Ketu": {"gem": "Cat’s Eye (Lehsunia)", "weight": "2 Carats", "metal": "Silver", "finger": "Middle finger",
             "mantra": "Om stram strim straum sah ketave namah"}
}

# Zodiac sign to planet mapping
sign_rulers = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
}

def get_moon_positions(dob_str, tob_str, place):
    
    from app.utils.calculate_chart import calculate_chart  

    chart = calculate_chart(dob_str, tob_str, place)

    return {
        "Ascendant": {"sign": chart["ascendant_sign"]},
        "Moon": {"sign": chart["moon_sign"]},
        "House_9": {"sign": chart["houses"][9]}  # 9th house sign
    }


@bp.route("/gemstone", methods=["POST"])
def gemstone_report():
    try:
        data = request.get_json()
        name = data.get("name")
        dob_str = data.get("dob")
        tob_str = data.get("tob")
        place = data.get("place")
        gender = data.get("gender")
        user_id = data.get("user_id")  # Ensure this is passed

        # Planetary positions
        positions = get_moon_positions(dob_str, tob_str, place)
        if not positions:
            return jsonify({"error": "Unable to calculate zodiac positions. Check birth details."}), 400

        asc_sign = positions.get("Ascendant", {}).get("sign")
        lagna_lord = sign_rulers.get(asc_sign)
        life_stone_info = gemstone_data.get(lagna_lord)

        moon_sign = positions.get("Moon", {}).get("sign")
        lucky_stone_planet = sign_rulers.get(moon_sign)
        lucky_stone_info = gemstone_data.get(lucky_stone_planet)

        ninth_house_sign = positions.get("House_9", {}).get("sign")
        ninth_lord = sign_rulers.get(ninth_house_sign)
        bhagya_stone_info = gemstone_data.get(ninth_lord)

        if not all([life_stone_info, lucky_stone_info, bhagya_stone_info]):
            return jsonify({"error": "Could not determine all gemstone recommendations."}), 400

        # Save to DB
        report = GemstoneReport(
            user_id=user_id,
            name=name,
            gender=gender,
            dob=dob_str,
            tob=tob_str,
            place=place,
            ascendant=asc_sign,
            moon_sign=moon_sign,
            house_9_sign=ninth_house_sign,
            life_stone=life_stone_info["gem"],
            lucky_stone=lucky_stone_info["gem"],
            bhagya_stone=bhagya_stone_info["gem"]
        )
        db.session.add(report)
        db.session.commit()

        response = {
            "life_stone": {
                "description": f"Since your Ascendant sign is {asc_sign}, ruled by {lagna_lord}, "
                               f"the life stone helps balance your personality and enhance your natural strengths.",
                "recommend_gemstone": life_stone_info["gem"],
                "minimum_weight": life_stone_info["weight"],
                "wearing_instructions": f"{life_stone_info['metal']}, in {life_stone_info['finger']}",
                "mantra": life_stone_info["mantra"]
            },
            "lucky_stone": {
                "description": f"With Moon in {moon_sign}, ruled by {lucky_stone_planet}, "
                               f"wearing this stone can strengthen emotional stability and bring mental peace.",
                "recommend_gemstone": lucky_stone_info["gem"],
                "minimum_weight": lucky_stone_info["weight"],
                "wearing_instructions": f"{lucky_stone_info['metal']}, in {lucky_stone_info['finger']}",
                "mantra": lucky_stone_info["mantra"]
            },
            "bhagya_stone": {
                "description": f"Your ninth house is in {ninth_house_sign}, ruled by {ninth_lord}, "
                               f"making this stone ideal for enhancing fortune, opportunities, and luck.",
                "recommend_gemstone": bhagya_stone_info["gem"],
                "minimum_weight": bhagya_stone_info["weight"],
                "wearing_instructions": f"{bhagya_stone_info['metal']}, in {bhagya_stone_info['finger']}",
                "mantra": bhagya_stone_info["mantra"]
            }
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
