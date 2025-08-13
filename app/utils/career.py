import random
from app.utils.calculate_chart import calculate_chart
from app.utils.nakshatra import generate_nakshatra_prediction
from app.models import CareerMapping
from app import db

def get_career_description(category, sign_or_house):
    record = CareerMapping.query.filter_by(category=category, sign_or_house=sign_or_house).first()
    return record.career_description if record else None

def expand_section(seed_texts, target_words=500):
    rng = random.Random()
    base_text = " ".join(seed_texts)
    filler_bank = [
        "This planetary combination not only influences your choices but also shapes how you approach challenges and opportunities.",
        "Over the years, these traits can guide you into roles where your natural abilities are both valued and rewarded.",
        "The alignment here points to a deeper calling that may become more apparent as you gain life experience.",
        "In different phases of your career, this combination may manifest in varied ways — from early experimentation to late mastery.",
        "This influence fosters resilience, adaptability, and a capacity to navigate complex professional landscapes.",
        "It also suggests that you may thrive in environments that value innovation, leadership, and a willingness to take calculated risks.",
        "Combined with your lunar placement and nakshatra traits, this can create a rich tapestry of skills and ambitions.",
    ]
    while len(base_text.split()) < target_words:
        base_text += " " + rng.choice(filler_bank)
    return base_text

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

    # Career section seeds
    career_seeds = [
        f"{name}, as a {ascendant} Ascendant with Moon in {moon_sign} and Nakshatra {nakshatra_name}, {personality}",
        f"Mercury in {mercury_sign} suggests {mercury_career}.",
        f"Mars in {mars_sign} adds {mars_career}.",
        f"Your 10th house in {tenth_house_sign} indicates {tenth_house_career}, and its lord in the {tenth_lord_house} house suggests {tenth_lord_career}.",
    ]
    career_text = expand_section(career_seeds, target_words=500)

    # Occupation section seeds
    occupation_seeds = [
        f"{name}, you excel in {', '.join(strengths)}.",
        f"Potential careers: {', '.join(career_options)}.",
        f"However, be mindful of {', '.join(weaknesses)}.",
        f"Your nakshatra influence gives you unique approaches to work and problem-solving."
    ]
    occupation_text = expand_section(occupation_seeds, target_words=500)

    # Finance section seeds
    finance_seeds = [
        f"Jupiter in {jupiter_sign} favours {jupiter_finance}.",
        f"Venus in {venus_sign} adds opportunities in {venus_finance}.",
        f"With your {', '.join(keywords)}, you attract opportunities especially after mid-30s."
    ]
    finance_text = expand_section(finance_seeds, target_words=500)

    return {
        "name": name,
        "ascendant": ascendant,
        "moon_sign": moon_sign,
        "nakshatra": nakshatra_name,
        "career": career_text,
        "occupation": occupation_text,
        "finance": finance_text
    }
