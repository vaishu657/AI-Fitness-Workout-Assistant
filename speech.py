from flask import Blueprint, request, jsonify
from speech_service import transcribe_file, tts_to_base64

speech_bp = Blueprint("speech", __name__, url_prefix="/api/speech")

@speech_bp.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"ok": False, "msg": "Send audio file in 'audio' field"}), 400
    audio = request.files["audio"]
    res = transcribe_file(audio.stream)
    return jsonify(res)

@speech_bp.route("/tts", methods=["POST"])
def tts():
    data = request.get_json() or {}
    text = data.get("text")
    if not text:
        return jsonify({"ok": False, "msg": "Missing text"}), 400
    b64 = tts_to_base64(text)
    return jsonify({"ok": True, "audio_base64": b64})

