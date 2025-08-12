from flask import Blueprint, request, jsonify
from app.utils.calculate_chart import calculate_chart
from app.utils.kundalichart import generate_kundli_image_jpg
from app.utils.mangal import check_mangal_dosh
from app import db
from app.models import MangalReport

bp = Blueprint("mangal", __name__)

@bp.route("/mangal", methods=["POST"])
def mangal_api():
    data = request.json
    name = data.get("name")
    dob = data.get("dob")
    tob = data.get("tob")
    place = data.get("place")
    user_id = data.get("user_id")

    try:
        # Step 1 – Calculate chart with planets and houses
        chart = calculate_chart(dob, tob, place)

        # Step 2 – Generate Moon Chart houses by shifting so Moon is 1st house
        moon_sign = chart["moon_sign"]
        moon_chart_houses = {}
        shift = list(chart["houses"].values()).index(moon_sign)
        for i, sign in enumerate(list(chart["houses"].values()), start=1):
            moon_chart_houses[((i - shift - 1) % 12) + 1] = sign

        # Step 3 – Check Mangal Dosh
        mangal_result = check_mangal_dosh(chart["houses"], moon_chart_houses, chart["planets"])

        # Step 4 – Prepare kundli data for chart image
        kundli_data = {
            "name": name,
            "dob": dob,
            "tob": tob,
            "place": place,
            "Ascendant": {"rashi": chart["ascendant_sign"]}
        }
        for planet, details in chart["planets"].items():
            kundli_data[planet] = {"rashi": details["sign"]}

        # Step 5 – Generate Lagna Kundali Image
        chart_img_base64 = generate_kundli_image_jpg(kundli_data, chart_type="lagna")

        # Step 6 add record in db
        report = MangalReport(
            user_id=user_id,
            name=name,
            dob=dob,
            tob=tob,
            place=place,
            ascendant=chart["ascendant_sign"],
            moon_sign=chart["moon_sign"],
            mangal_present=mangal_result["present"],
            severity=mangal_result["severity"],
            details=mangal_result["details"]
        )
        db.session.add(report)
        db.session.commit()

        # Step 7 – Return JSON response
        return jsonify({
            "ascendant": chart["ascendant_sign"],
            "moon_sign": chart["moon_sign"],
            "mangal_present": mangal_result["present"],
            "severity": mangal_result["severity"],
            "details": mangal_result["details"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
