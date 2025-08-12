from datetime import datetime
from geopy.geocoders import Nominatim
import swisseph as swe
from app.models import Nakshatra, Pada
import json

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

def generate_nakshatra_prediction(dob, tob, place):
    geolocator = Nominatim(user_agent="nakshatra_api")
    location = geolocator.geocode(place)

    if not location:
        return {"error": "Location not found."}

    # Combine DOB and TOB
    dt_str = f"{dob} {tob}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    
    # Get Julian Day
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

    # Set geographic location for swisseph
    swe.set_topo(location.longitude, location.latitude, 0)

    # Get Moon's position
    moon_pos = swe.calc_ut(jd, swe.MOON)[0]
    moon_long = moon_pos[0]

    # Calculate nakshatra index (27 divisions of 13°20′)
    nakshatra_index = int(moon_long // (360 / 27))
    nakshatra_name = NAKSHATRAS[nakshatra_index]

    # Calculate pada (4 padas of 3°20′ in each nakshatra)
    pada = int((moon_long % (360 / 27)) // (360 / 108)) + 1  # 108 padas in total

    nakshatra = Nakshatra.query.filter_by(name=nakshatra_name).first()
    if not nakshatra:
        return {"error": f"Nakshatra '{nakshatra_name}' not found in database."}

    # Query Pada from DB
    pada_data = Pada.query.filter_by(nakshatra_id=nakshatra.id, pada_number=pada).first()
    if not pada_data:
        return {"error": f"No data available for {nakshatra_name} Pada {pada} in database."}

    return {
        "nakshatra": nakshatra.name,
        "pada": pada_data.pada_number,
        "personality": pada_data.personality,
        "strengths": json.loads(pada_data.strengths),
        "weaknesses": json.loads(pada_data.weaknesses),
        "career": json.loads(pada_data.career),
        "emotional_traits": pada_data.emotional_traits,
        "ideal_partner": pada_data.ideal_partner,
        "keywords": json.loads(nakshatra.keywords)
    }
