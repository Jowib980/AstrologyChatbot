from flask import Blueprint, jsonify
from app.models import Service

bp = Blueprint('services', __name__)

@bp.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    data = []
    for s in services:
        data.append({
            "card_id": s.card_id,
            "title": s.title,
            "img": s.img,
            "description": s.description,
            "route": s.route,
            "fields": s.fields.split(",") if s.fields else [],
            "link": s.link
        })
    return jsonify(data)
