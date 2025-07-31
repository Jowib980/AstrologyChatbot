from flask import Blueprint, request, jsonify
from datetime import datetime
from geopy.geocoders import Nominatim
from skyfield.api import load, Topos
import traceback
from app.utils.kundalichart import generate_kundli_image_jpg

bp = Blueprint("kundali", __name__)

rashi_names = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def degrees_to_sign(degrees):
    return rashi_names[int(degrees // 30)]

def predict_life_events(kundli):
    predictions = []

    if kundli.get("Venus", {}).get("rashi") in ["Pisces", "Libra"]:
        predictions.append("Your love life may be strong and fulfilling.")
    if kundli.get("Saturn", {}).get("rashi") in ["Capricorn", "Aquarius"]:
        predictions.append("Career will be stable and grow steadily with time.")
    if kundli.get("Moon", {}).get("rashi") == "Scorpio":
        predictions.append("You may experience emotional intensity and deep inner growth.")
    if kundli.get("Sun", {}).get("rashi") == "Leo":
        predictions.append("Natural leadership ability and charisma will guide your life.")

    return predictions

def generate_kundli(dob, tob, place):
    try:
        # 1. Get coordinates from place
        geolocator = Nominatim(user_agent="kundli_bot")
        location = geolocator.geocode(place, timeout=10)
        if not location:
            return {"error": "Invalid location"}

        # 2. Load ephemeris and time
        planets = load('de440s.bsp')
        ts = load.timescale()
        birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        t = ts.utc(birth_dt.year, birth_dt.month, birth_dt.day, birth_dt.hour, birth_dt.minute)

        # 3. Define observer
        observer = planets["earth"] + Topos(latitude_degrees=location.latitude, longitude_degrees=location.longitude)

        # 4. Main planet calculations
        planet_map = {
            "Sun": planets["sun"],
            "Moon": planets["moon"],
            "Mercury": planets["mercury"],
            "Venus": planets["venus"],
        }

        kundli = {}
        for name, planet in planet_map.items():
            ecliptic = observer.at(t).observe(planet).apparent().ecliptic_latlon()
            lon = ecliptic[1].degrees
            kundli[name] = {
                "degree": round(lon % 30, 2),
                "rashi": degrees_to_sign(lon)
            }

        # 5. Rahu and Ketu
        moon = planets["moon"]
        earth = planets["earth"]
        node = (observer.at(t).observe(moon).apparent().ecliptic_latlon()[1].degrees + 180) % 360
        kundli["Rahu"] = {
            "degree": round(node % 30, 2),
            "rashi": degrees_to_sign(node)
        }
        ketu = (node + 180) % 360
        kundli["Ketu"] = {
            "degree": round(ketu % 30, 2),
            "rashi": degrees_to_sign(ketu)
        }

        # 6. Ascendant (Lagna) – approx by using Sun’s rising
        asc = observer.at(t).from_altaz(alt_degrees=0, az_degrees=90).ecliptic_latlon()[1].degrees
        kundli["Ascendant"] = {
            "degree": round(asc % 30, 2),
            "rashi": degrees_to_sign(asc)
        }

        # 7. Optional predictions
        kundli["predictions"] = predict_life_events(kundli)

        return kundli

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

def get_navamsa_rashi(degree):
    sign_index = int(degree // 30)
    pada = int((degree % 30) // 3.3333)  # 9 Navamsa padas in 30°
    navamsa_sign = (sign_index * 9 + pada) % 12
    return rashi_names[navamsa_sign]

def generate_kundli_with_navamsa(dob, tob, place):
    base_chart = generate_kundli(dob, tob, place)
    if "error" in base_chart:
        return base_chart

    navamsa_chart = {}
    for planet, data in base_chart.items():
        if planet in ["name", "gender", "dob", "tob", "place", "chart_image_base64", "predictions"]:
            continue
        degree = data["degree"] + rashi_names.index(data["rashi"]) * 30
        navamsa_chart[planet] = {
            "degree": round(degree % 30, 2),
            "rashi": get_navamsa_rashi(degree)
        }

    return {
        "lagna_chart": base_chart,
        "navamsa_chart": navamsa_chart
    }

@bp.route('/kundali', methods=['POST'])
def api_kundli():
    try:
        data = request.get_json(force=True)
        name = data.get("name")
        gender = data.get("gender")
        dob = data.get("dob")
        tob = data.get("tob")
        place = data.get("place")

        if not dob or not tob or not place:
            return jsonify({"error": "Missing dob, tob, or place"}), 400

        charts = generate_kundli_with_navamsa(dob, tob, place)
        if "error" in charts:
            return jsonify(charts), 400

        # Add common metadata
        for chart in [charts["lagna_chart"], charts["navamsa_chart"]]:
            chart.update({
                "name": name,
                "gender": gender,
                "dob": dob,
                "tob": tob,
                "place": place
            })

        # Generate images
        charts["lagna_chart"]["chart_image_base64"] = generate_kundli_image_jpg(charts["lagna_chart"], chart_type="lagna")
        charts["navamsa_chart"]["chart_image_base64"] = generate_kundli_image_jpg(charts["navamsa_chart"], chart_type="navamsa")

        return jsonify(charts)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
