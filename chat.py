from flask import Blueprint, request, jsonify
from ..services.nlp_service import parse_message, generate_reply
from ..models import Exercise
from ..extensions import db

# Define Blueprint
chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")

# Route inside the blueprint
@chat_bp.route("", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "")

    # Parse message using NLP
    parsed = parse_message(message or "")

    # Query exercises based on parsed data
    q = Exercise.query
    if parsed.get("location"):
        q = q.filter(Exercise.location.ilike(f"%{parsed['location']}%"))
    if parsed.get("goal"):
        q = q.filter(Exercise.goal.ilike(f"%{parsed['goal']}%"))
    if parsed.get("duration"):
        q = q.filter(Exercise.duration <= parsed["duration"])

    exercises = q.limit(20).all()
    exercises_json = [e.to_dict() for e in exercises]

    # Generate AI reply
    reply = generate_reply(message)

    return jsonify({
        "reply": reply,
        "parsed": parsed,
        "exercises": exercises_json
    })
