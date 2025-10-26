import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from posture_service import analyze_image

posture_bp = Blueprint("posture", __name__, url_prefix="/api/posture")

ALLOWED_EXT = {"png", "jpg", "jpeg", "bmp", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@posture_bp.route("", methods=["POST"])
def posture():
    if "image" in request.files:
        file = request.files["image"]
        if not file or file.filename == "":
            return jsonify({"ok": False, "msg": "No file"}), 400
        if not allowed_file(file.filename):
            return jsonify({"ok": False, "msg": "Unsupported file type"}), 400
        filename = secure_filename(file.filename)
        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)
        path = os.path.join(upload_dir, filename)
        file.save(path)
        result = analyze_image(path)
        return jsonify(result)
    else:
        return jsonify({"ok": False, "msg": "Send multipart form with 'image' file"}), 400



