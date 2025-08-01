from skyfield.api import load, Topos
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim

ZODIAC_SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

lagna_lords = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
    'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}

character_traits = {
    'Aries': {
        'core': ["bold", "action-oriented", "highly ambitious"],
        'strengths': ["courage in adversity", "leadership", "quick decisions"],
        'challenges': ["impulsiveness", "lack of patience", "dominance"],
        'ruled_by': "Mars",
        'happiness': "You find happiness in challenges, leadership roles, and independence.",
        'fulfillment': "You feel fulfilled when you're winning, pioneering, or making an impact.",
        'lifestyle': "Active, energetic, goal-oriented. Needs physical activity and excitement."
    },
    'Taurus': {
        'core': ["stable", "practical", "sensual"],
        'strengths': ["consistency", "patience", "loyalty"],
        'challenges': ["stubbornness", "material fixation", "resistance to change"],
        'ruled_by': "Venus",
        'happiness': "You find happiness in comfort, routine, and sensory pleasures.",
        'fulfillment': "You feel fulfilled when building long-term security and nurturing relationships.",
        'lifestyle': "Grounded and steady. Enjoys routine, beauty, and nature-based living."
    },
    'Gemini': {
        'core': ["curious", "versatile", "communicative"],
        'strengths': ["intelligence", "adaptability", "social connection"],
        'challenges': ["restlessness", "indecisiveness", "surface-level interests"],
        'ruled_by': "Mercury",
        'happiness': "You find happiness in learning, talking, and staying mentally stimulated.",
        'fulfillment': "You feel fulfilled when expressing yourself and connecting ideas or people.",
        'lifestyle': "Fast-paced, mentally active, and full of variety. Needs freedom and stimulation."
    },
    'Cancer': {
        'core': ["nurturing", "emotional", "protective"],
        'strengths': ["empathy", "loyalty", "intuition"],
        'challenges': ["moodiness", "over-sensitivity", "clinginess"],
        'ruled_by': "Moon",
        'happiness': "You find happiness in emotional security, home, and family bonds.",
        'fulfillment': "You feel fulfilled when caring for others and creating a safe haven.",
        'lifestyle': "Home-loving, sentimental, and family-centered. Needs emotional comfort and privacy."
    },
    'Leo': {
        'core': ["confident", "charismatic", "creative"],
        'strengths': ["leadership", "generosity", "warmth"],
        'challenges': ["pride", "need for validation", "stubbornness"],
        'ruled_by': "Sun",
        'happiness': "You find happiness in being admired, creating, and leading.",
        'fulfillment': "You feel fulfilled when expressing your talents and making others feel special.",
        'lifestyle': "Dramatic, expressive, and regal. Needs recognition and opportunities to shine."
    },
    'Virgo': {
        'core': ["analytical", "precise", "humble"],
        'strengths': ["problem-solving", "attention to detail", "reliability"],
        'challenges': ["overthinking", "criticism", "perfectionism"],
        'ruled_by': "Mercury",
        'happiness': "You find happiness in order, productivity, and useful routines.",
        'fulfillment': "You feel fulfilled when improving something or being of service.",
        'lifestyle': "Organized, clean, health-focused. Needs meaningful work and routines."
    },
    'Libra': {
        'core': ["diplomatic", "charming", "graceful"],
        'strengths': ["fairness", "aesthetic sense", "sociability"],
        'challenges': ["indecisiveness", "people-pleasing", "avoidance of conflict"],
        'ruled_by': "Venus",
        'happiness': "You find happiness in harmony, art, and close companionship.",
        'fulfillment': "You feel fulfilled when helping others find balance and beauty.",
        'lifestyle': "Balanced, elegant, partnership-driven. Needs connection and beauty around."
    },
    'Scorpio': {
        'core': ["intense", "mysterious", "passionate"],
        'strengths': ["emotional depth", "determination", "loyalty"],
        'challenges': ["possessiveness", "jealousy", "extremes"],
        'ruled_by': "Mars",
        'happiness': "You find happiness in emotional truth, deep bonds, and personal power.",
        'fulfillment': "You feel fulfilled when you transform, heal, or uncover deeper meaning.",
        'lifestyle': "Private, intense, focused. Needs trust, intensity, and inner purpose."
    },
    'Sagittarius': {
        'core': ["adventurous", "optimistic", "philosophical"],
        'strengths': ["honesty", "broad vision", "exploration"],
        'challenges': ["bluntness", "overconfidence", "restlessness"],
        'ruled_by': "Jupiter",
        'happiness': "You find happiness in travel, new ideas, and freedom.",
        'fulfillment': "You feel fulfilled when pursuing knowledge and sharing wisdom.",
        'lifestyle': "Nomadic, exploratory, freedom-seeking. Needs space and inspiration."
    },
    'Capricorn': {
        'core': ["disciplined", "ambitious", "pragmatic"],
        'strengths': ["responsibility", "persistence", "strategic thinking"],
        'challenges': ["rigidity", "workaholism", "emotional restraint"],
        'ruled_by': "Saturn",
        'happiness': "You find happiness in achievement, control, and meaningful structure.",
        'fulfillment': "You feel fulfilled when building legacy and earning respect.",
        'lifestyle': "Structured, high-achieving, and reserved. Needs purpose and goals."
    },
    'Aquarius': {
        'core': ["innovative", "independent", "idealistic"],
        'strengths': ["originality", "vision", "humanitarianism"],
        'challenges': ["detachment", "aloofness", "rebelliousness"],
        'ruled_by': "Saturn",
        'happiness': "You find happiness in progress, innovation, and meaningful causes.",
        'fulfillment': "You feel fulfilled when working toward future-oriented ideals.",
        'lifestyle': "Unconventional, tech-savvy, cause-driven. Needs freedom and mental stimulation."
    },
    'Pisces': {
        'core': ["dreamy", "compassionate", "imaginative"],
        'strengths': ["intuition", "creativity", "empathy"],
        'challenges': ["escapism", "oversensitivity", "lack of boundaries"],
        'ruled_by': "Jupiter",
        'happiness': "You find happiness in creative expression and emotional connection.",
        'fulfillment': "You feel fulfilled when helping others or expressing your dreams.",
        'lifestyle': "Flowy, artistic, spiritual. Needs inspiration and emotional space."
    }
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


def build_character_sections(sign):
    traits = character_traits[sign]

    character = (
        f"As a {sign}, you are {traits['core'][0]}, {traits['core'][1]}, and {traits['core'][2]}. "
        f"Your strengths include {traits['strengths'][0]}, {traits['strengths'][1]}, and {traits['strengths'][2]}. "
        f"However, you may struggle with {traits['challenges'][0]}, {traits['challenges'][1]}, and {traits['challenges'][2]}. "
        f"Ruled by {traits['ruled_by']}, you possess a strong connection to your inner drive and purpose."
    )

    return {
        "character": character,
        "happiness": traits["happiness"],
        "fulfillment": traits["fulfillment"],
        "lifestyle": traits["lifestyle"]
    }



def get_character_prediction(dob, tob, place):
    lagna = get_lagna_sign(dob, tob, place)
    lagna_lord = lagna_lords[lagna]
    sections = build_character_sections(lagna)

    return {
        "lagna": lagna,
        "lagna_lord": lagna_lord,
        **sections
    }
