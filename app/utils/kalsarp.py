from app.utils.calculate_chart import ZODIAC_SIGNS
from app.utils.kundalichart import generate_kundli_image_jpg

def check_kalsarp_dosh(planets):
    sign_index = {s: i for i, s in enumerate(ZODIAC_SIGNS)}
    rahu_pos = sign_index[planets["Rahu"]["sign"]]
    ketu_pos = sign_index[planets["Ketu"]["sign"]]

    main_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    planet_positions = [sign_index[planets[p]["sign"]] for p in main_planets]

    clockwise_range = [(rahu_pos + i) % 12 for i in range((ketu_pos - rahu_pos) % 12)]
    anticlockwise_range = [(ketu_pos + i) % 12 for i in range((rahu_pos - ketu_pos) % 12)]

    if all(pos in clockwise_range for pos in planet_positions):
        return True, "Kaal Sarp Dosh present (Clockwise) – All planets between Rahu and Ketu."
    elif all(pos in anticlockwise_range for pos in planet_positions):
        return True, "Kaal Sarp Dosh present (Anti-clockwise) – All planets between Rahu and Ketu."
    return False, "No Kaal Sarp Dosh"
