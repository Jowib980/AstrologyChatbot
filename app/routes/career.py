# routes.py
from flask import request, jsonify, Blueprint
from app.utils.career import generate_career_details

bp = Blueprint('career', __name__)

@bp.route('/career', methods=['POST'])
def career_api():
    data = request.json
    result = generate_career_details(
        name=data['name'],
        dob=data['dob'],
        tob=data['tob'],
        place=data['place'],
        gender=data.get('gender', '')
    )
    return jsonify(result)
