# career.py
from app.utils.calculate_chart import calculate_chart
from app.utils.nakshatra import generate_nakshatra_prediction
from datetime import datetime

MERCURY_CAREER = {
    "Aries": "sales, marketing, entrepreneurship, fast-paced business ventures",
    "Taurus": "finance, banking, arts, luxury goods",
    "Gemini": "writing, teaching, journalism, public speaking",
    "Cancer": "real estate, hospitality, counselling",
    "Leo": "leadership, politics, event management",
    "Virgo": "data analysis, accounting, research",
    "Libra": "law, diplomacy, fashion design",
    "Scorpio": "investigation, research, psychology, surgery",
    "Sagittarius": "education, law, travel industry",
    "Capricorn": "administration, corporate leadership, engineering",
    "Aquarius": "technology, innovation, social causes",
    "Pisces": "arts, music, healing professions"
}

MARS_CAREER = {
    "Aries": "defense, sports, startup founder roles",
    "Taurus": "construction, real estate, banking",
    "Gemini": "media, transport, marketing",
    "Cancer": "catering, home-based businesses, property",
    "Leo": "politics, army, leadership",
    "Virgo": "engineering, medical professions",
    "Libra": "partnership businesses, legal work",
    "Scorpio": "military intelligence, surgery, research",
    "Sagittarius": "sports coaching, adventure tourism",
    "Capricorn": "project management, heavy industry",
    "Aquarius": "technology startups, activism",
    "Pisces": "creative arts, charity work"
}

JUPITER_FINANCE = {
    "Aries": "business ventures, leadership roles",
    "Taurus": "banking, luxury trade, investments",
    "Gemini": "media, communication-related businesses",
    "Cancer": "real estate, family business",
    "Leo": "government contracts, high-profile roles",
    "Virgo": "service industries, analytics",
    "Libra": "law, diplomacy, art dealing",
    "Scorpio": "research, speculative investments",
    "Sagittarius": "education, publishing, travel",
    "Capricorn": "corporate sector, administration",
    "Aquarius": "technology, innovative industries",
    "Pisces": "spiritual services, creative industries"
}

VENUS_FINANCE = {
    "Aries": "fashion, design, entertainment",
    "Taurus": "luxury goods, beauty industry",
    "Gemini": "advertising, media",
    "Cancer": "home decor, catering",
    "Leo": "film industry, event management",
    "Virgo": "jewelry, accounting",
    "Libra": "art, partnerships",
    "Scorpio": "investments, mining, luxury real estate",
    "Sagittarius": "tourism, cultural trade",
    "Capricorn": "real estate, corporate finance",
    "Aquarius": "tech startups, digital art",
    "Pisces": "music, cinema, healing arts"
}

TENTH_HOUSE_CAREER = {
    "Aries": "leadership roles, military, sports, entrepreneurship",
    "Taurus": "finance, arts, agriculture, luxury goods",
    "Gemini": "writing, journalism, teaching, marketing",
    "Cancer": "real estate, hospitality, caregiving professions",
    "Leo": "politics, management, entertainment",
    "Virgo": "research, medicine, accounting",
    "Libra": "law, diplomacy, fashion",
    "Scorpio": "investigation, surgery, occult sciences",
    "Sagittarius": "education, law, travel",
    "Capricorn": "administration, engineering, corporate sector",
    "Aquarius": "technology, innovation, social service",
    "Pisces": "arts, spirituality, healing"
}

TENTH_LORD_PLACEMENT = {
    "1st": "self-employed or personal brand-based career",
    "2nd": "family business, finance, wealth management",
    "3rd": "media, communication, transport",
    "4th": "real estate, agriculture, home-based business",
    "5th": "arts, entertainment, speculation",
    "6th": "service industry, law, healthcare",
    "7th": "business partnerships, law, diplomacy",
    "8th": "research, psychology, insurance",
    "9th": "teaching, publishing, travel",
    "10th": "government roles, high authority positions",
    "11th": "technology, networking, NGOs",
    "12th": "foreign trade, hospitals, spiritual work"
}


def generate_career_details(name, dob, tob, place, gender):
    zodiac_data = calculate_chart(dob, tob, place)
    print(zodiac_data)
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

    # --- Career ---
    career_line = f"Mercury in {mercury_sign} suggests {MERCURY_CAREER.get(mercury_sign, 'versatile skills')}. " \
                  f"Mars in {mars_sign} adds {MARS_CAREER.get(mars_sign, 'energy and leadership')}. " \
                  f"Your 10th house in {tenth_house_sign} indicates {TENTH_HOUSE_CAREER.get(tenth_house_sign, 'diverse career opportunities')}, " \
                  f"and its lord placed in the {tenth_lord_house} house suggests {TENTH_LORD_PLACEMENT.get(tenth_lord_house, 'a flexible career path')}."

    career_text = f"{name}, as a {ascendant} Ascendant with Moon in {moon_sign} and Nakshatra {nakshatra_name}, " \
                  f"{personality} In your chart, {career_line}"

    # --- Occupation ---
    occupation_text = f"{name}, you excel in {', '.join(strengths)}. " \
                      f"Potential careers: {', '.join(career_options)}. " \
                      f"However, be mindful of {', '.join(weaknesses)}."

    # --- Finance ---
    finance_line = f"Jupiter in {jupiter_sign} favours {JUPITER_FINANCE.get(jupiter_sign, 'business growth')}. " \
                   f"Venus in {venus_sign} adds opportunities in {VENUS_FINANCE.get(venus_sign, 'creative ventures')}."

    finance_text = f"{name}, your financial growth benefits from {finance_line} " \
                   f"With your {', '.join(keywords)}, you attract opportunities especially after mid-30s."

    return {
        "name": name,
        "ascendant": ascendant,
        "moon_sign": moon_sign,
        "nakshatra": nakshatra_name,
        "career": career_text,
        "occupation": occupation_text,
        "finance": finance_text
    }
