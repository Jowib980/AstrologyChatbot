from flask import Blueprint, request, jsonify
from app.utils.calculate_chart import calculate_chart
from app.utils.kundalichart import generate_kundli_image_jpg
from app.utils.kalsarp import check_kalsarp_dosh

bp = Blueprint("kalsarp", __name__)

@bp.route("/kalsarp", methods=["POST"])
def kalsarp_api():
    data = request.json
    name = data.get("name")
    dob = data.get("dob")
    tob = data.get("tob")
    place = data.get("place")

    try:
        # Step 1 – Calculate chart with planets
        chart = calculate_chart(dob, tob, place)

        # Step 2 – Check Kaal Sarp Dosh
        has_dosh, message = check_kalsarp_dosh(chart["planets"])

        # Step 3 – Add required chart details for image generation
        kundli_data = {
            "name": name,
            "dob": dob,
            "tob": tob,
            "place": place,
            "Ascendant": {"rashi": chart["ascendant_sign"]}
        }
        for planet, details in chart["planets"].items():
            kundli_data[planet] = {"rashi": details["sign"]}


        # Step 4 – Generate Lagna Kundali Image
        chart_img_base64 = generate_kundli_image_jpg(kundli_data, chart_type="lagna")

        # Step 5 – Return JSON response
        return jsonify({
            "name": name,
            "ascendant": chart["ascendant_sign"],
            "moon_sign": chart["moon_sign"],
            "kalsarp_present": has_dosh,
            "message": message,
            "lagna_chart_base64": chart_img_base64
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
