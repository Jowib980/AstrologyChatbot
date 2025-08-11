from app.models import TransitInterpretation

def generate_gochar_report(natal_chart, transits):
    lagna_sign = natal_chart["ascendant_sign"]
    report = []

    for planet, transit_sign in transits.items():
        house_num = get_house_from_lagna(lagna_sign, transit_sign)
        
        # Query the DB for the interpretation
        interp_obj = TransitInterpretation.query.filter_by(planet=planet, house_number=house_num).first()
        if interp_obj:
            text = interp_obj.interpretation
        else:
            text = ""

        report.append({
            "planet": planet,
            "sign": transit_sign,
            "house": house_num,
            "interpretation": text
        })

    return report
