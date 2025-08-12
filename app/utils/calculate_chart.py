from datetime import datetime
from geopy.geocoders import Nominatim
import swisseph as swe
from pytz import timezone, UTC

# List of zodiac signs
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def get_location_coordinates(place):
    """Get latitude & longitude from place name."""
    geolocator = Nominatim(user_agent="kundli_calc")
    location = geolocator.geocode(place, timeout=10)
    if not location:
        raise ValueError(f"Could not find location for: {place}")
    return location.latitude, location.longitude

def calculate_chart(dob_str, tob_str, place):
    SIGN_LORDS = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }

    # Parse date/time
    dob = datetime.strptime(dob_str, "%Y-%m-%d")
    hour, minute = map(int, tob_str.split(":"))
    dob = dob.replace(hour=hour, minute=minute)

    # Get coordinates
    lat, lon = get_location_coordinates(place)

    # Convert to Julian Day in UT
    tz = timezone("Asia/Kolkata")
    local_dt = tz.localize(dob)
    utc_dt = local_dt.astimezone(UTC)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                    utc_dt.hour + utc_dt.minute / 60.0)

    # Handle both return formats of houses_ex
    houses_result = swe.houses_ex(jd, lat, lon, b'P')
    if len(houses_result) == 3:
        ascmc, cusps, _ = houses_result
    else:
        cusps, ascmc = houses_result

    asc_long = ascmc[0]
    asc_sign = ZODIAC_SIGNS[int(asc_long // 30)]

    # Moon position
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    if isinstance(moon_long, (list, tuple)):
        moon_long = moon_long[0]
    moon_sign = ZODIAC_SIGNS[int(moon_long // 30)]

    # House signs
    houses = {}
    for house_num in range(1, 13):
        house_long = cusps[house_num - 1]
        houses[house_num] = ZODIAC_SIGNS[int(house_long // 30)]

    # Planet positions
    planet_ids = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS,
        "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE, "Ketu": swe.MEAN_NODE
    }
    planets = {}
    for pname, pid in planet_ids.items():
        pl_long, _ = swe.calc_ut(jd, pid)
        if isinstance(pl_long, (list, tuple)):
            pl_long = pl_long[0]
        sign = ZODIAC_SIGNS[int(pl_long // 30)]
        planets[pname] = {"sign": sign}
    # Adjust Ketu to be opposite Rahu
    planets["Ketu"]["sign"] = ZODIAC_SIGNS[(ZODIAC_SIGNS.index(planets["Rahu"]["sign"]) + 6) % 12]

    # 10th house sign & lord
    tenth_house_sign = houses[10]
    tenth_house_lord = SIGN_LORDS[tenth_house_sign]

    # Find which house the lord is placed in
    tenth_lord_house = None
    lord_sign = planets[tenth_house_lord]["sign"]
    for hnum, sign in houses.items():
        if sign == lord_sign:
            tenth_lord_house = hnum
            break

    return {
        "ascendant_sign": asc_sign,
        "moon_sign": moon_sign,
        "houses": houses,
        "planets": planets,
        "houses_info": {
            "10th": {
                "sign": tenth_house_sign,
                "lord": tenth_house_lord,
                "lord_house": str(tenth_lord_house) if tenth_lord_house else None
            }
        }
    }
