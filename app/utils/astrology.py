from datetime import datetime
from geopy.geocoders import Nominatim
from skyfield.api import load, Topos

def ra_to_sign(ra_str):
    hour = int(ra_str.split('h')[0])
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    return signs[hour // 2]

def get_zodiac_positions(dob, tob, place):
    try:
        geolocator = Nominatim(user_agent="astro_bot")
        location = geolocator.geocode(place, timeout=10)
        if not location:
            return None

        planets = load('de440s.bsp')
        ts = load.timescale()
        birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        t = ts.utc(birth_dt.year, birth_dt.month, birth_dt.day, birth_dt.hour, birth_dt.minute)

        observer = planets["earth"] + Topos(latitude_degrees=location.latitude, longitude_degrees=location.longitude)

        planet_names = {
            "Sun": 10,
            "Moon": 301,
            "Mercury": 199,
            "Venus": 299,
        }

        result = {}
        for name, code in planet_names.items():
            astrometric = observer.at(t).observe(planets[code]).apparent()
            ra, _, _ = astrometric.radec()
            result[name] = ra_to_sign(str(ra))

        return result
    except Exception as e:
        print("Error:", e)
        return None

def parse_time_string(t):
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(t, fmt).time()
        except ValueError:
            continue
    raise ValueError("Invalid time format")

def calculate_health_index(zodiac_positions):
    score = 50
    good_moon_signs = ["Taurus", "Cancer"]
    if zodiac_positions.get("Moon") in good_moon_signs:
        score += 20
    fiery_signs = ["Aries", "Leo", "Sagittarius"]
    if zodiac_positions.get("Sun") in fiery_signs:
        score += 15
    strong_mercury_signs = ["Virgo", "Gemini"]
    if zodiac_positions.get("Mercury") in strong_mercury_signs:
        score += 10
    strong_venus_signs = ["Libra", "Taurus"]
    if zodiac_positions.get("Venus") in strong_venus_signs:
        score += 5
    score = max(0, min(score, 100))
    return score
