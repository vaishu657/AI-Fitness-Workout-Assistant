import os
from flask import Flask, send_from_directory
from config import Config
from backend.extensions import db, migrate, cors
from backend.models import User, Exercise

def create_app():
    app = Flask(
        __name__, 
        static_folder=os.path.join(os.path.dirname(__file__), "frontend"), 
        static_url_path="/"
    )
    app.config.from_object(Config)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Register routes
    from backend.routes.auth import auth_bp
    from backend.routes.exercises import exercises_bp
    from backend.routes.chat import chat_bp
    from backend.routes.posture import posture_bp
    from backend.routes.speech import speech_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(exercises_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(posture_bp)
    app.register_blueprint(speech_bp)

    # Serve frontend
    @app.route("/")
    def index():
        index_path = os.path.join(app.static_folder or "", "index.html")
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, "index.html")
        return {"ok": True, "msg": "Backend running"}

    return app


def seed_db(app):
    with app.app_context():
        if Exercise.query.first():
            return
        examples = [
            {"name": "Chair Squats", "location": "office", "equipment": "none", "goal": "strength", "duration": 5,
             "description": "Stand and sit back to the chair slowly, then stand up."},
            {"name": "Desk Push-ups", "location": "office", "equipment": "desk", "goal": "strength", "duration": 5,
             "description": "Hands on desk, lean forward and push away."},
            {"name": "Jumping Jacks", "location": "home", "equipment": "none", "goal": "cardio", "duration": 3,
             "description": "Classic jumping jacks."},
            {"name": "Plank", "location": "home", "equipment": "none", "goal": "strength", "duration": 2,
             "description": "Hold plank position with straight body."},
            {"name": "Yoga Cat-Cow", "location": "home", "equipment": "none", "goal": "flexibility", "duration": 4,
             "description": "Move between arching and rounding your back."},
        ]
        for it in examples:
            e = Exercise(**it)
            db.session.add(e)
        db.session.commit()
        print("✅ Seeded default exercises.")


if __name__ == "__main__":
    app = create_app()
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    with app.app_context():
        db.create_all()
        seed_db(app)
    app.run(debug=True, host="127.0.0.1", port=5000)
