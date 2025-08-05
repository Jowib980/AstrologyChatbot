from flask import Blueprint, request, jsonify
from app.utils.calculate_chart import calculate_chart
from app.utils.ascendant import generate_ascendant_traits

bp = Blueprint("ascendant", __name__)

@bp.route("/ascendant", methods=["POST"])
def ascendant_api():
    data = request.json
    name = data.get("name")
    dob = data.get("dob")
    tob = data.get("tob")
    place = data.get("place")

    try:
        # Calculate chart
        chart = calculate_chart(dob, tob, place)
        ascendant_sign = chart["ascendant_sign"]

        # Dynamically generate traits
        traits = generate_ascendant_traits(ascendant_sign)
        if not traits:
            return jsonify({
                "name": name,
                "ascendant": ascendant_sign,
                "error": f"No traits found for {ascendant_sign}"
            }), 404

        return jsonify({
            "name": name,
            "ascendant": ascendant_sign,
            **traits
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
