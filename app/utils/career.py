# career.py
from app.utils.calculate_chart import calculate_chart
from app.utils.nakshatra import generate_nakshatra_prediction
from datetime import datetime
from app.models import CareerMapping
from app import db

def get_career_description(category, sign_or_house):
    record = CareerMapping.query.filter_by(category=category, sign_or_house=sign_or_house).first()
    if record:
        return record.career_description
    else:
        return None


def generate_career_details(name, dob, tob, place, gender):
    zodiac_data = calculate_chart(dob, tob, place)
    ascendant = zodiac_data['ascendant_sign']
    moon_sign = zodiac_data['moon_sign']
    planets = zodiac_data['planets']
    tenth_house_sign = zodiac_data['houses_info']['10th']['sign']
    tenth_lord_house = zodiac_data['houses_info']['10th']['lord_house']

    nakshatra_info = generate_nakshatra_prediction(dob, tob, place)
    nakshatra_name = nakshatra_info['nakshatra']
    personality = nakshatra_info['personality']
    strengths = nakshatra_info['strengths']
    weaknesses = nakshatra_info['weaknesses']
    career_options = nakshatra_info['career']
    keywords = nakshatra_info['keywords']

    mercury_sign = planets['Mercury']['sign']
    mars_sign = planets['Mars']['sign']
    jupiter_sign = planets['Jupiter']['sign']
    venus_sign = planets['Venus']['sign']

    mercury_career = get_career_description("Mercury", mercury_sign) or "versatile skills"
    mars_career = get_career_description("Mars", mars_sign) or "energy and leadership"
    tenth_house_career = get_career_description("TenthHouse", tenth_house_sign) or "diverse career opportunities"
    tenth_lord_career = get_career_description("TenthLord", tenth_lord_house) or "a flexible career path"
    jupiter_finance = get_career_description("Jupiter", jupiter_sign) or "business growth"
    venus_finance = get_career_description("Venus", venus_sign) or "creative ventures"

    career_line = (
        f"Mercury in {mercury_sign} suggests {mercury_career}. "
        f"Mars in {mars_sign} adds {mars_career}. "
        f"Your 10th house in {tenth_house_sign} indicates {tenth_house_career}, "
        f"and its lord placed in the {tenth_lord_house} house suggests {tenth_lord_career}."
    )

    career_text = (
        f"{name}, as a {ascendant} Ascendant with Moon in {moon_sign} and Nakshatra {nakshatra_name}, "
        f"{personality} In your chart, {career_line}"
    )

    occupation_text = (
        f"{name}, you excel in {', '.join(strengths)}. "
        f"Potential careers: {', '.join(career_options)}. "
        f"However, be mindful of {', '.join(weaknesses)}."
    )

    finance_line = (
        f"Jupiter in {jupiter_sign} favours {jupiter_finance}. "
        f"Venus in {venus_sign} adds opportunities in {venus_finance}."
    )

    finance_text = (
        f"{name}, your financial growth benefits from {finance_line} "
        f"With your {', '.join(keywords)}, you attract opportunities especially after mid-30s."
    )

    return {
        "name": name,
        "ascendant": ascendant,
        "moon_sign": moon_sign,
        "nakshatra": nakshatra_name,
        "career": career_text,
        "occupation": occupation_text,
        "finance": finance_text
    }
