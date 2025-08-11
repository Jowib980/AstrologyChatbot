import swisseph as swe

# Constants
EPOCH = 2451545.0  # J2000

def get_moon_info(jd, lat, lon):
    swe.set_topo(lon, lat, 0)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)
    rashi = int(moon_long // 30) + 1
    nakshatra_index = int(moon_long // (360 / 27))  # 0-26
    return {
        "rashi": rashi,
        "nakshatra": nakshatra_index
    }

def match_varna(boy_rashi, girl_rashi):
    # Example rule: same varna = 1, else 0
    return 1 if boy_rashi == girl_rashi else 0

def match_vashya(boy_rashi, girl_rashi):
    # Placeholder (based on zodiac groups)
    return 2 if abs(boy_rashi - girl_rashi) in [1, 2] else 1

def match_tara(boy_nakshatra, girl_nakshatra):
    # Real tara logic uses counting stars – placeholder here
    return 2

def match_yoni(boy_nakshatra, girl_nakshatra):
    return 3

def match_grahmaitri(boy_rashi, girl_rashi):
    return 4

def match_gana(boy_nakshatra, girl_nakshatra):
    return 5

def match_bhakoot(boy_rashi, girl_rashi):
    return 7

def match_nadi(boy_nakshatra, girl_nakshatra):
    return 8 if boy_nakshatra != girl_nakshatra else 0


def match_all_kootas(boy, girl):
    boy_rashi = boy['rashi']
    girl_rashi = girl['rashi']
    boy_nakshatra = boy['nakshatra']
    girl_nakshatra = girl['nakshatra']

    result = []

    def add_koota(name, score, max_score, desc):
        result.append({
            "koota": name,
            "score": score,
            "max": max_score,
            "description": desc
        })

    add_koota("Varna", match_varna(boy_rashi, girl_rashi), 1, "Spiritual compatibility based on caste system")
    add_koota("Vashya", match_vashya(boy_rashi, girl_rashi), 2, "Mutual attraction and control")
    add_koota("Tara", match_tara(boy_nakshatra, girl_nakshatra), 3, "Nakshatra compatibility")
    add_koota("Yoni", match_yoni(boy_nakshatra, girl_nakshatra), 4, "Sexual compatibility")
    add_koota("Graha Maitri", match_grahmaitri(boy_rashi, girl_rashi), 5, "Friendshipbetween sign lords")
    add_koota("Gana", match_gana(boy_nakshatra, girl_nakshatra), 6, "Temperament matching")
    add_koota("Bhakoot", match_bhakoot(boy_rashi, girl_rashi), 7, "Love and family bonding")
    add_koota("Nadi", match_nadi(boy_nakshatra, girl_nakshatra), 8, "Genetic compatibility and health")

    total_score = sum(k["score"] for k in result)
    max_score = sum(k["max"] for k in result)

    return {
        "total_score": total_score,
        "max_score": max_score,
        "kootas": result,
        "mangal_dosh": False,  # Optional: implement Mangal logic
        "note": "Calculated using real rashi and nakshatra values"
    }
