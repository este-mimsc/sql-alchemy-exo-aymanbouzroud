from flask import Flask, request, jsonify
from models import db, User, Post

def create_app(config=None):
    app = Flask(__name__)

    # Configuration par défaut
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///blog.db")
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # Configuration de test (pour pytest)
    if config:
        app.config.update(config)

    db.init_app(app)

    # Créer les tables au démarrage
    with app.app_context():
        db.create_all()

    # ---------------- ROUTES ---------------- #

    @app.get("/users")
    def list_users():
        users = User.query.all()
        return jsonify([u.to_dict() for u in users]), 200

    @app.post("/users")
    def create_user():
        data = request.get_json()
        if not data or "username" not in data:
            return jsonify({"error": "username is required"}), 400

        user = User(username=data["username"])
        db.session.add(user)
        db.session.commit()

        return jsonify(user.to_dict()), 201

    @app.get("/posts")
    def list_posts():
        posts = Post.query.all()
        return jsonify([p.to_dict() for p in posts]), 200

    @app.post("/posts")
    def create_post():
        data = request.get_json()
        if not data or "title" not in data or "user_id" not in data:
            return jsonify({"error": "title and user_id required"}), 400

        user = User.query.get(data["user_id"])
        if not user:
            return jsonify({"error": "Invalid user_id"}), 400

        post = Post(title=data["title"], user_id=data["user_id"])
        db.session.add(post)
        db.session.commit()

        return jsonify(post.to_dict()), 201

    return app
