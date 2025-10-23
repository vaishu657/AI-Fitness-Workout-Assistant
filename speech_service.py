import os
import io
import base64
from gtts import gTTS
import speech_recognition as sr
from tempfile import NamedTemporaryFile

def transcribe_file(file_stream, file_type=None):
    r = sr.Recognizer()
    with NamedTemporaryFile(delete=True, suffix=".wav") as tmp:
        tmp.write(file_stream.read())
        tmp.flush()
        with sr.AudioFile(tmp.name) as source:
            audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            return {"ok": True, "text": text}
        except sr.UnknownValueError:
            return {"ok": False, "error": "Could not understand audio"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

def tts_to_base64(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    with NamedTemporaryFile(delete=True, suffix=".mp3") as tmp:
        tts.write_to_fp(open(tmp.name, "wb"))
        tmp.flush()
        b = open(tmp.name, "rb").read()
        return base64.b64encode(b).decode("utf-8")
