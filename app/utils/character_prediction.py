from skyfield.api import load, Topos
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
from app.models import CharacterSign, CharacterTrait
from app import db

ZODIAC_SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

lagna_lords = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
    'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}


def get_lagna_sign(dob, tob, place):
    eph = load('de421.bsp')
    ts = load.timescale()
    geolocator = Nominatim(user_agent="astro-api")
    location = geolocator.geocode(place)
    latitude, longitude = location.latitude, location.longitude

    dt_str = f"{dob} {tob}"
    birth_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    tz = pytz.timezone("Asia/Kolkata")
    birth_dt = tz.localize(birth_dt)
    t = ts.from_datetime(birth_dt)

    observer = eph['earth'] + Topos(latitude_degrees=latitude, longitude_degrees=longitude)
    astrological_degrees = (observer.at(t).observe(eph['earth']).apparent().altaz()[1].degrees + 360) % 360
    sign_index = int(astrological_degrees // 30)
    return ZODIAC_SIGNS[sign_index]


def fetch_character_traits_from_db(sign):
    sign_obj = CharacterSign.query.filter_by(name=sign).first()
    if not sign_obj:
        return None

    traits_map = {trait.trait_type: trait.description for trait in sign_obj.traits}
    traits_map['ruled_by'] = sign_obj.ruled_by
    return traits_map


def build_character_sections(sign):
    traits = fetch_character_traits_from_db(sign)
    if not traits:
        return None  # Or some default message or fallback

    # For traits stored as comma-separated strings, split them back to lists if needed
    def to_list(value):
        return [x.strip() for x in value.split(",")] if value else []

    core = to_list(traits.get('core', ''))
    strengths = to_list(traits.get('strengths', ''))
    challenges = to_list(traits.get('challenges', ''))

    character = (
        f"As a {sign}, you are {', '.join(core)}. "
        f"Your strengths include {', '.join(strengths)}. "
        f"However, you may struggle with {', '.join(challenges)}. "
        f"Ruled by {traits.get('ruled_by', 'your ruling planet')}, you possess a strong connection to your inner drive and purpose."
    )

    return {
        "character": character,
        "happiness": traits.get("happiness", ""),
        "fulfillment": traits.get("fulfillment", ""),
        "lifestyle": traits.get("lifestyle", "")
    }


def get_character_prediction(dob, tob, place):
    lagna = get_lagna_sign(dob, tob, place)
    lagna_lord = lagna_lords.get(lagna, "Unknown")
    sections = build_character_sections(lagna) or {}

    return {
        "lagna": lagna,
        "lagna_lord": lagna_lord,
        **sections
    }
