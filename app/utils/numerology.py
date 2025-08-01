# numerology.py
from datetime import datetime
import re

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

numerology_data = {
    1: {
        "favourable_sign": "Leo",
        "favourable_alphabets": "A, I, J, Q, Y",
        "gemstone": "Ruby",
        "favourable_days": "Sunday, Monday",
        "favourable_number": "1, 3, 10, 19, 28",
        "direction": "East",
        "auspicious_color": "Red, Orange",
        "ruling_planet": "Sun",
        "god_goddess": "Surya (Sun God)",
        "fast": "Sunday",
        "favourable_dates": "1st, 10th, 19th, 28th",
        "mantra": "ॐ घृणिः सूर्याय नमः"
    },
    2: {
        "favourable_sign": "Cancer",
        "favourable_alphabets": "B, K, R",
        "gemstone": "Pearl",
        "favourable_days": "Monday, Friday",
        "favourable_number": "2, 11, 20, 29",
        "direction": "North-West",
        "auspicious_color": "White, Cream",
        "ruling_planet": "Moon",
        "god_goddess": "Parvati, Chandra Dev",
        "fast": "Monday",
        "favourable_dates": "2nd, 11th, 20th, 29th",
        "mantra": "ॐ चन्द्राय नमः"
    },
    3: {
        "favourable_sign": "Sagittarius, Pisces",
        "favourable_alphabets": "C, G, L, S",
        "gemstone": "Yellow Sapphire",
        "favourable_days": "Thursday, Sunday",
        "favourable_number": "3, 12, 21, 30",
        "direction": "North-East",
        "auspicious_color": "Yellow, Gold",
        "ruling_planet": "Jupiter",
        "god_goddess": "Brihaspati, Vishnu",
        "fast": "Thursday",
        "favourable_dates": "3rd, 12th, 21st, 30th",
        "mantra": "ॐ बृं बृहस्पतये नमः"
    },
    4: {
        "favourable_sign": "Aquarius",
        "favourable_alphabets": "D, M, T",
        "gemstone": "Hessonite (Gomed)",
        "favourable_days": "Saturday, Sunday",
        "favourable_number": "4, 13, 22, 31",
        "direction": "South-West",
        "auspicious_color": "Electric Blue, Grey",
        "ruling_planet": "Rahu",
        "god_goddess": "Durga, Lord Ganesha",
        "fast": "Saturday",
        "favourable_dates": "4th, 13th, 22nd, 31st",
        "mantra": "ॐ रां राहवे नमः"
    },
    5: {
        "favourable_sign": "Gemini, Virgo",
        "favourable_alphabets": "E, H, N, X",
        "gemstone": "Emerald",
        "favourable_days": "Wednesday, Friday",
        "favourable_number": "5, 14, 23",
        "direction": "North",
        "auspicious_color": "Green, Light Blue",
        "ruling_planet": "Mercury",
        "god_goddess": "Narayan, Vishnu",
        "fast": "Wednesday",
        "favourable_dates": "5th, 14th, 23rd",
        "mantra": "ॐ बुं बुधाय नमः"
    },
    6: {
        "favourable_sign": "Taurus, Libra",
        "favourable_alphabets": "U, V, W",
        "gemstone": "Diamond",
        "favourable_days": "Friday, Tuesday",
        "favourable_number": "6, 15, 24",
        "direction": "South-East",
        "auspicious_color": "Pink, White",
        "ruling_planet": "Venus",
        "god_goddess": "Lakshmi, Shukracharya",
        "fast": "Friday",
        "favourable_dates": "6th, 15th, 24th",
        "mantra": "ॐ शुं शुक्राय नमः"
    },
    7: {
        "favourable_sign": "Pisces, Cancer",
        "favourable_alphabets": "O, Z",
        "gemstone": "Cat’s Eye",
        "favourable_days": "Monday, Thursday",
        "favourable_number": "7, 16, 25",
        "direction": "West",
        "auspicious_color": "Violet, Purple",
        "ruling_planet": "Ketu",
        "god_goddess": "Ganesh, Lord Shiva",
        "fast": "Tuesday",
        "favourable_dates": "7th, 16th, 25th",
        "mantra": "ॐ कें केतवे नमः"
    },
    8: {
        "favourable_sign": "Capricorn, Aquarius",
        "favourable_alphabets": "F, P",
        "gemstone": "Blue Sapphire",
        "favourable_days": "Saturday, Wednesday",
        "favourable_number": "8, 17, 26",
        "direction": "South",
        "auspicious_color": "Dark Blue, Black",
        "ruling_planet": "Saturn",
        "god_goddess": "Shani Dev, Hanuman",
        "fast": "Saturday",
        "favourable_dates": "8th, 17th, 26th",
        "mantra": "ॐ शं शनैश्चराय नमः"
    },
    9: {
        "favourable_sign": "Aries, Scorpio",
        "favourable_alphabets": "M, T",
        "gemstone": "Coral",
        "favourable_days": "Tuesday, Sunday",
        "favourable_number": "9, 18, 27",
        "direction": "South",
        "auspicious_color": "Red, Maroon",
        "ruling_planet": "Mars",
        "god_goddess": "Hanuman, Durga",
        "fast": "Tuesday",
        "favourable_dates": "9th, 18th, 27th",
        "mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः"
    }
}

# Destiny and Name meanings can be similar or extended later

def generate_numerology_report(name, dob):
    radical = get_radical_number(dob)
    destiny = get_destiny_number(dob)
    name_no = get_name_number(name)

    return {
        "name": name,
        "dob": dob,
        "radical_number": radical,
        "radical_meaning": radical_meanings.get(radical, "Not defined."),
        "destiny_number": destiny,
        "destiny_meaning": radical_meanings.get(destiny, "Not defined."),
        "name_number": name_no,
        "name_meaning": radical_meanings.get(name_no, "Not defined.")
    }
