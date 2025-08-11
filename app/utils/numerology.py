from datetime import datetime
import re
from app.models import NumerologyNumber

# Pythagorean letter to number mapping
LETTER_TO_NUMBER = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

def reduce_to_single_digit(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(map(int, str(n)))
    return n

def get_radical_number(dob_str):
    day = int(dob_str.split('-')[2])
    return reduce_to_single_digit(day)

def get_destiny_number(dob_str):
    total = sum(map(int, re.sub(r'[^0-9]', '', dob_str)))
    return reduce_to_single_digit(total)

def get_name_number(name):
    total = 0
    for char in name.upper():
        if char in LETTER_TO_NUMBER:
            total += LETTER_TO_NUMBER[char]
    return reduce_to_single_digit(total)

def calculate_radical_number(day: int) -> int:
    return sum(int(d) for d in str(day)) % 9 or 9


radical_meanings = {
    1: "Independent, leader, ambitious, original thinker.",
    2: "Diplomatic, sensitive, cooperative, peace-loving.",
    3: "Creative, expressive, social, optimistic.",
    4: "Practical, hardworking, disciplined, stable.",
    5: "Adventurous, versatile, energetic, freedom-loving.",
    6: "Responsible, nurturing, family-oriented, artistic.",
    7: "Introspective, intellectual, spiritual, analytical.",
    8: "Powerful, authoritative, goal-driven, materialistic.",
    9: "Compassionate, humanitarian, emotional, idealistic."
}


def generate_numerology_report(name, dob):
    radical = get_radical_number(dob)
    destiny = get_destiny_number(dob)
    name_no = get_name_number(name)

    # Fetch data from DB for each number
    radical_entry = NumerologyNumber.query.filter_by(number=radical).first()
    destiny_entry = NumerologyNumber.query.filter_by(number=destiny).first()
    name_entry = NumerologyNumber.query.filter_by(number=name_no).first()

    def entry_to_dict(entry):
        if not entry:
            return {}
        return {
            "favourable_sign": entry.favourable_sign,
            "favourable_alphabets": entry.favourable_alphabets,
            "gemstone": entry.gemstone,
            "favourable_days": entry.favourable_days,
            "favourable_number": entry.favourable_number,
            "direction": entry.direction,
            "auspicious_color": entry.auspicious_color,
            "ruling_planet": entry.ruling_planet,
            "god_goddess": entry.god_goddess,
            "fast": entry.fast,
            "favourable_dates": entry.favourable_dates,
            "mantra": entry.mantra,
            "personality": entry.personality,
            "career": entry.career,
            "dos": [dos.advice for dos in entry.dos],
            "donts": [dont.advice for dont in entry.donts],
            "compatibles": [comp.compatible_number for comp in entry.compatibles]
        }

    return {
        "name": name,
        "dob": dob,
        "radical_number": radical,
        "radical_data": entry_to_dict(radical_entry),
        "destiny_number": destiny,
        "destiny_data": entry_to_dict(destiny_entry),
        "name_number": name_no,
        "name_data": entry_to_dict(name_entry),
        "radical_meaning": radical_meanings.get(radical, "Not defined."),
        "destiny_meaning": radical_meanings.get(destiny, "Not defined."),
        "name_meaning": radical_meanings.get(name_no, "Not defined.")
    }
