from flask import Blueprint, request, jsonify
from app.utils.astrology import get_zodiac_positions
from app.utils.ai import generate_answer, format_prompt
from app.models import User, db

bp = Blueprint("chatbot", __name__)

@bp.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_id = data.get("user_id")
    prompt = format_prompt(
        data["name"],
        data["dob"],
        data["time"],
        data["place"],
        data["question"]
    )
    if prompt is None:
        return jsonify({"answer": "Could not calculate planetary positions due to missing data."})

    answer = generate_answer(prompt)

    chat = ChatHistory(
        user_id=user_id,
        name=data["name"],
        dob=data["dob"],
        time=data["time"],
        place=data["place"],
        question=data["question"],
        answer=answer
    )
    db.session.add(chat)
    db.session.commit()

    return jsonify({"answer": answer})

@bp.route('/history/<int:user_id>', methods=['GET'])
def get_user_history(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    history = ChatHistory.query.filter_by(user_id=user_id).order_by(ChatHistory.timestamp.asc()).all()

    if history:
        latest = history[-1]
        dob = latest.dob
        birth_time = latest.time
        birth_place = latest.place
    else:
        dob = None
        birth_time = None
        birth_place = None

    history_data = [
        {"question": item.question, "answer": item.answer, "timestamp": item.timestamp.isoformat()}
        for item in history
    ]

    return jsonify({
        "user": {
            "name": user.name,
            "dob": dob,
            "birth_time": birth_time,
            "birth_place": birth_place
        },
        "history": history_data
    })
