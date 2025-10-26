from flask import Blueprint, request, jsonify
from extensions import db
from models import Exercise

# 🔹 Rename bp → exercises_bp
exercises_bp = Blueprint("exercises", __name__, url_prefix="/api/exercises")

@exercises_bp.route("", methods=["GET"])
def list_exercises():
    location = request.args.get("location")
    duration = request.args.get("duration", type=int)
    goal = request.args.get("goal")
    q = Exercise.query
    if location:
        q = q.filter(Exercise.location.ilike(f"%{location}%"))
    if goal:
        q = q.filter(Exercise.goal.ilike(f"%{goal}%"))
    if duration:
        q = q.filter(Exercise.duration <= duration)
    items = q.limit(100).all()
    return jsonify([e.to_dict() for e in items])

@exercises_bp.route("", methods=["POST"])
def create_exercise():
    data = request.get_json() or {}
    e = Exercise(
        name=data.get("name"),
        location=data.get("location"),
        equipment=data.get("equipment"),
        goal=data.get("goal"),
        duration=data.get("duration"),
        description=data.get("description"),
    )
    db.session.add(e)
    db.session.commit()
    return jsonify({"ok": True, "exercise": e.to_dict()})

