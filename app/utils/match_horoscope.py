import swisseph as swe
import pytz
from datetime import datetime
from geopy.geocoders import Nominatim

# Nakshatra list (27)
nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

# Rashi list (12 zodiac signs)
rashis = [
    "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
    "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"
]

def get_location_coordinates(place):
    geolocator = Nominatim(user_agent="kundali_matcher")
    location = geolocator.geocode(place)
    if location:
        return location.latitude, location.longitude
    else:
        raise Exception(f"Could not find coordinates for: {place}")

def get_julian_day(dob_str, tob_str, place):
    dt_str = f"{dob_str} {tob_str}"
    local = pytz.timezone('Asia/Kolkata')
    local_dt = local.localize(datetime.strptime(dt_str, "%Y-%m-%d %H:%M"))
    utc_dt = local_dt.astimezone(pytz.utc)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)
    return jd

def get_moon_rashi_nakshatra(dob_str, tob_str, place):
    lat, lon = get_location_coordinates(place)
    jd = get_julian_day(dob_str, tob_str, place)
    moon_pos = swe.calc_ut(jd, swe.MOON)[0]

    # Moon longitude in degrees
    moon_long = moon_pos[0]

    # Nakshatra calculation
    nakshatra_index = int(moon_long / (360 / 27))
    nakshatra = nakshatras[nakshatra_index]

    # Rashi (sign) calculation
    rashi_index = int(moon_long / 30)
    rashi = rashis[rashi_index]

    return {
        "moon_long": moon_long,
        "nakshatra": nakshatra,
        "rashi": rashi
    }
