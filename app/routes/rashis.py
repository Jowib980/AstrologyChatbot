from flask import Blueprint, jsonify
from app.models import Rashis

bp = Blueprint('rashis', __name__)

@bp.route('/rashis', methods=['GET'])
def get_rashis():
    rashis = Rashis.query.all()
    data = []
    for s in rashis:
        data.append({
            "card_id": s.card_id,
            "icon": s.icon,
            "title": s.title,
            "img": s.img,
            "description": s.description,
            "route": s.route,
            "short_description": s.short_description
        })
    return jsonify(data)

@bp.route('/rashi/<route>', methods=['GET'])
def get_rashi_by_route(route):
    rashi = Rashis.query.filter_by(route=route).first()
    if not rashi:
        return jsonify({"error": "Rashi not found"}), 404   
    
    return jsonify({
        "title": rashi.title,
        "img": rashi.img,
        "description": rashi.description,
        "short_description": rashi.short_description
    })
