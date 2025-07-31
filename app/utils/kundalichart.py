from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
from geopy.geocoders import Nominatim
import os

JPG_PATH = "app/static/"

def get_chart_style(place):
    geolocator = Nominatim(user_agent="kundli_chart")
    location = geolocator.geocode(place, timeout=10)
    if not location:
        return "north"

    south_states = ["Tamil Nadu", "Karnataka", "Andhra", "Telangana", "Kerala"]
    address = location.raw.get("display_name", "")
    for state in south_states:
        if state.lower() in address.lower():
            return "south"
    return "north"

def generate_kundli_image_jpg(kundli_data, chart_type="lagna"):

    chart_type = get_chart_style(kundli_data["place"])
    template_file = "kundali_south.jpg" if chart_type == "south" else "kundali_north.jpg"
    template_path = os.path.join(JPG_PATH, template_file)

    # Load image template
    img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Load fonts
    font_path = "arial.ttf"
    bold_font_path = "arialbd.ttf"

    try:
        font = ImageFont.truetype(font_path, 26)
        bold_font = ImageFont.truetype(bold_font_path, 28)
    except:
        font= ImageFont.load_default()
        bold_font = font

    # House positions
    house_positions = {
        "north": {
            1: (420, 175),
            2: (210, 125), 
            3: (75, 225),
            4: (220, 450),
            5: (75, 670),
            6: (220, 790),
            9: (765, 670),
            8: (620, 790),
            7: (420, 660),
            10: (635, 450),
            11: (765, 225),
            12: (620, 105),
        },
        "south": {
            1:  (370, 230),
            2: (655, 230),   
            3: (890, 230),
            4:  (890, 470),  
            5: (890, 760),  
            6: (890, 985),
            7:  (660, 985), 
            8: (370, 985),  
            9: (165, 985),
            10: (165, 760), 
            11: (165, 470), 
            12: (165, 230)
        }
    }

    positions = house_positions[chart_type]

    rashi_symbols = {
        "Aries": "♈", "Taurus": "♉", "Gemini": "♊", "Cancer": "♋",
        "Leo": "♌", "Virgo": "♍", "Libra": "♎", "Scorpio": "♏",
        "Sagittarius": "♐", "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓"
    }

    # Get Lagna (Ascendant)
    rashi_names = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    lagna_rashi = kundli_data["Ascendant"]["rashi"]
    lagna_index = rashi_names.index(lagna_rashi)

    # Map rashis to house numbers
    house_for_rashi = {}
    for i in range(12):
        rashi = rashi_names[i]
        house = ((i - lagna_index + 12) % 12) + 1
        house_for_rashi[rashi] = house

    # Draw house numbers (optional)
    for house_num, (x, y) in positions.items():
        draw.text((x, y - 25), f"H{house_num}", fill="gray", font=font)

    for rashi, house in house_for_rashi.items():
        x, y = positions[house]
        draw.text((x + 35, y - 45), rashi_symbols.get(rashi, ""), font=font, fill="darkblue")

    planet_colors = {
        "Sun": "orange", "Moon": "blue", "Mercury": "green",
        "Venus": "deeppink", "Mars": "red", "Jupiter": "gold",
        "Saturn": "gray", "Rahu": "purple", "Ketu": "brown"
    }

    # Draw planets
    planet_offsets = {
        "Sun": (0, 0), "Moon": (0, 20), "Mercury": (0, 40),
        "Venus": (0, 60), "Mars": (0, 80), "Jupiter": (0, 100),
        "Saturn": (0, 120), "Rahu": (0, 140), "Ketu": (0, 160),
    }

    planet_counts = {}  # to track offset stacking

    for planet, data in kundli_data.items():
        if planet in ["name", "gender", "dob", "tob", "place", "chart_image_base64", "predictions"]:
            continue
        rashi = data["rashi"]
        house = house_for_rashi[rashi]
        x, y = positions[house]

        if house not in planet_counts:
            planet_counts[house] = 0
        y_offset = planet_counts[house] * 18
        draw.text((x, y + y_offset), planet, fill=planet_colors.get(planet, "black"), font=font)
        planet_counts[house] += 1

    # Draw Lagna in bold red
    lagna_x, lagna_y = positions[1]
    draw.text((lagna_x, lagna_y - 50), "Lagna", fill="darkred", font=bold_font)

    # Save to base64
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=90)
    b64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return b64_image
