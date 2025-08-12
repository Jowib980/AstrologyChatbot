import swisseph as swe
import datetime

swe.set_ephe_path("ephe")  # update this path to match your actual setup

rashi_names = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def generate_kundli(date, time, lat, lon):
    try:
        dt = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

        planets = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mercury': swe.MERCURY,
            'Venus': swe.VENUS,
            'Mars': swe.MARS,
            'Jupiter': swe.JUPITER,
            'Saturn': swe.SATURN,
            'Rahu': swe.MEAN_NODE,
            'Ketu': swe.MEAN_NODE
        }

        kundli = {}

        for planet, pid in planets.items():
            position, _ = swe.calc_ut(jd, pid)
            lon_ = position[0]
            if planet == "Ketu":
                lon_ = (lon_ + 180) % 360
            rashi_index = int(lon_ // 30)
            kundli[planet] = {
                'degree': round(lon_ % 30, 2),
                'rashi': rashi_names[rashi_index]
            }

        asc = swe.houses(jd, lat, lon)[0][0]
        asc_index = int(asc // 30)
        kundli["Ascendant"] = {
            "degree": round(asc % 30, 2),
            "rashi": rashi_names[asc_index]
        }

        return kundli
    except Exception as e:
        return {"error": str(e)}
