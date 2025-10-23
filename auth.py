from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"ok": False, "msg": "Missing username or password"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"ok": False, "msg": "Username taken"}), 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"ok": True, "user": user.to_dict()})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"ok": False, "msg": "Invalid credentials"}), 401
    return jsonify({"ok": True, "user": user.to_dict()})
