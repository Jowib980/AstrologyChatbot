from flask import Blueprint, request, jsonify
from app.utils.astrology import get_zodiac_positions
from app.utils.nakshatra import generate_nakshatra_prediction, nakshatra_traits

bp = Blueprint('love', __name__)

# Venus traits by sign
def describe_venus_traits(sign):
    traits = {
        "Aries": "Confident, energetic, enthusiastic, independent, impulsive, passionate, direct, spontaneous in love and sometimes impatient",
        "Taurus": "romantic, sensual, and loyal",
        "Gemini": "playful, witty, and intellectually curious",
        "Cancer": "nurturing, protective, and emotionally deep",
        "Leo": "dramatic, affectionate, and warm-hearted",
        "Virgo": "thoughtful, attentive, and detail-oriented",
        "Libra": "graceful, charming, and relationship-focused",
        "Scorpio": "intense, magnetic, and emotionally powerful",
        "Sagittarius": "adventurous, open-hearted, and freedom-loving",
        "Capricorn": "reserved, committed, and loyal in a practical way",
        "Aquarius": "unconventional, detached but loyal, and freedom-loving",
        "Pisces": "dreamy, romantic, and emotionally intuitive"
    }
    return traits.get(sign, "unique and complex in love")

# Mars traits by sign
def describe_mars_traits(sign):
    traits = {
        "Aries": "bold, energetic, and impulsive",
        "Taurus": "steady, sensual, and persistent",
        "Gemini": "versatile, flirty, and communicative",
        "Cancer": "emotionally driven, protective, and moody",
        "Leo": "passionate, proud, and expressive",
        "Virgo": "precise, thoughtful, and reserved",
        "Libra": "charming, balanced, and diplomatic",
        "Scorpio": "intense, powerful, and magnetic",
        "Sagittarius": "adventurous, independent, and restless",
        "Capricorn": "disciplined, strategic, and patient",
        "Aquarius": "original, unpredictable, and rational",
        "Pisces": "imaginative, sensitive, and romantic"
    }
    return traits.get(sign, "dynamic in your own way")

# Main love paragraph generator
def generate_love_text(name, gender, nakshatra, pada, planets, nakshatra_info):
    moon_sign = planets.get("Moon", "Unknown")
    venus_sign = planets.get("Venus", "Unknown")
    mars_sign = planets.get("Mars", "Unknown")

    personality = nakshatra_info.get("personality", "insightful and unique")
    emotional = nakshatra_info.get("emotional_traits", "emotionally intense and receptive")
    partner = nakshatra_info.get("ideal_partner", "emotionally supportive and compatible")

    intro = f"{name}, your emotional world is influenced by the Moon in {moon_sign}, giving you a {emotional.lower()} nature."
    
    marriage_tone = (
        "You are likely to attract a partner who is expressive and emotionally understanding."
        if gender.lower() == "female"
        else "You are drawn to partners who are nurturing and intellectually stimulating."
    )

    venus_traits = f"With Venus in {venus_sign}, your love style is {describe_venus_traits(venus_sign)}."
    mars_traits = f"Your Mars in {mars_sign} makes you {describe_mars_traits(mars_sign)} in relationships."

    return f"""
{name}, you are meant to experience deep and meaningful relationships. Solitude may drain your energy, and companionship brings out the best in you. Based on your Nakshatra (**{nakshatra}**, Pada {pada}) and planetary placements, your emotional style blends intensity with affection.

💖 **Emotional Traits:** {emotional}
💑 **Ideal Partner Traits:** {partner}

✨ **Nakshatra Personality Insight:** {personality}
🌙 **Moon Sign Insight:** {intro}
💘 **Venus in Love:** {venus_traits}
🔥 **Mars in Passion:** {mars_traits}

{marriage_tone} A tastefully arranged and emotionally secure home environment is essential for your romantic happiness.
""".strip()

# Flask route
@bp.route('/love', methods=['POST'])
def love_prediction():
    data = request.get_json()
    name = data.get("name")
    dob = data.get("dob")
    tob = data.get("tob")
    place = data.get("place")
    gender = data.get("gender")

    if not all([name, dob, tob, place, gender]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        nakshatra_data = generate_nakshatra_prediction(dob, tob, place)
        if not nakshatra_data:
            return jsonify({"error": "Could not determine Nakshatra"}), 500

        nakshatra = nakshatra_data["nakshatra"]
        pada = nakshatra_data["pada"]

        planets = get_zodiac_positions(dob, tob, place)
        print("DEBUG PLANETS:", planets)

        print("Incoming Nakshatra:", nakshatra)
        print("Incoming Pada:", pada)

        nakshatra_info = nakshatra_traits.get(nakshatra, {}).get("padas", {}).get(int(pada))
        if not nakshatra_info:
            print(f"[WARN] Missing traits for {nakshatra} Pada {pada}, using fallback.")
            nakshatra_info = {
                "personality": "unique and complex",
                "emotional_traits": "emotionally nuanced and expressive",
                "ideal_partner": "emotionally understanding and supportive"
            }
        print(f"DEBUG TRAITS for {nakshatra} Pada {pada}: {nakshatra_info}")


        love_text = generate_love_text(name, gender, nakshatra, pada, planets, nakshatra_info)

        return jsonify({
            "name": name,
            "nakshatra": nakshatra,
            "pada": pada,
            "love_prediction": love_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
