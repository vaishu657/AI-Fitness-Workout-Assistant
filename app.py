import os
from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db, migrate
from models import User, Exercise

def create_app():
    app = Flask(__name__)
    
    # Configuration for production
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
    
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register routes
    from auth import auth_bp
    from exercises import exercises_bp
    from chat import chat_bp
    from posture import posture_bp
    from speech import speech_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(exercises_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(posture_bp, url_prefix='/api')
    app.register_blueprint(speech_bp, url_prefix='/api')

    # Health check routes
    @app.route("/")
    def index():
        return jsonify({"ok": True, "msg": "AI Fitness Workout Assistant API"})
    
    @app.route("/api/health")
    def health():
        return jsonify({"status": "healthy", "message": "Backend is running"})

    return app

# ✅ CREATE THE APP VARIABLE AT MODULE LEVEL FOR GUNICORN
app = create_app()

def seed_db():
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

# Only run this when executing the file directly, not when imported by Gunicorn
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
