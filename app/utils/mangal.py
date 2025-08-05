
def check_mangal_dosh(houses, moon_houses, planets):
    """
    Checks Manglik Dosha from both Lagna Chart & Moon Chart
    and returns a detailed astrologer-style result.
    """

    # Manglik houses (commonly used set)
    manglik_houses = [1, 4, 7, 8, 12]

    mars_sign = planets["Mars"]["sign"]

    # Find Mars house in Lagna Chart
    mars_house_lagna = next((h for h, s in houses.items() if s == mars_sign), None)

    # Find Mars house in Moon Chart
    mars_house_moon = next((h for h, s in moon_houses.items() if s == mars_sign), None)

    # Determine presence
    mangal_in_lagna_chart = mars_house_lagna in manglik_houses
    mangal_in_moon_chart = mars_house_moon in manglik_houses

    # Build result text
    if mangal_in_lagna_chart and not mangal_in_moon_chart:
        severity = "Low"
        chart_presence = "Lagna Chart only"
        presence_text = (
            f"Generally Manglik Dosha is considered from the position of Lagna and Moon in the birth chart. "
            f"In the birth chart, Mangal is placed in {mars_house_lagna}th house from Lagna, "
            f"while in the Moon chart Mangal is placed in {mars_house_moon}th house.\n\n"
            "Hence Mangal Dosha is present in Lagna Chart but not in Moon Chart. "
        )
    elif mangal_in_lagna_chart and mangal_in_moon_chart:
        severity = "High"
        chart_presence = "Both Lagna and Moon Charts"
        presence_text = (
            f"Generally Manglik Dosha is considered from the position of Lagna and Moon in the birth chart. "
            f"In the birth chart, Mangal is placed in {mars_house_lagna}th house from Lagna "
            f"and in {mars_house_moon}th house from Moon.\n\n"
            "Hence Mangal Dosha is strongly present in both Lagna and Moon charts, which is considered more impactful "
            "for married life."
        )
    elif not mangal_in_lagna_chart and mangal_in_moon_chart:
        severity = "Low"
        chart_presence = "Moon Chart only"
        presence_text = (
            f"Person is Manglik ({severity}).\n"
            f"Generally Manglik Dosha is considered from the position of Lagna and Moon in the birth chart. "
            f"In the birth chart, Mangal is placed in {mars_house_lagna}th house from Lagna, "
            f"while in the Moon chart Mangal is placed in {mars_house_moon}th house.\n\n"
            "Hence Mangal Dosha is present in Moon Chart but not in Lagna Chart."
        )
    else:
        severity = "None"
        presence_text = (
            f"Generally Manglik Dosha is considered from the position of Lagna and Moon in the birth chart. "
            f"In the birth chart, Mangal is placed in {mars_house_lagna}th house from Lagna "
            f"and in {mars_house_moon}th house from Moon.\n\n"
            "Hence Mangal Dosha is not present in both Lagna and Moon charts."
        )

    return {
        "present": severity != "None",
        "severity": severity,
        "details": presence_text
    }
