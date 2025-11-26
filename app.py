from flask import Flask, request, jsonify
from models import db, User, Post
import os


def create_app():
    app = Flask(__name__)

    # Configuration BDD
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///blog.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Crée les tables
    with app.app_context():
        db.create_all()

    # -----------------------
    # ROUTES USERS
    # -----------------------

    @app.get("/users")
    def list_users():
        users = User.query.all()
        return jsonify([u.to_dict() for u in users]), 200

    @app.post("/users")
    def create_user():
        data = request.get_json()

        if not data or "username" not in data:
            return jsonify({"error": "username is required"}), 400

        username = data["username"].strip()

        if username == "":
            return jsonify({"error": "username cannot be empty"}), 400

        # Vérifie si username existe déjà
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "username already exists"}), 400

        user = User(username=username)
        db.session.add(user)
        db.session.commit()

        return jsonify(user.to_dict()), 201

    # -----------------------
    # ROUTES POSTS
    # -----------------------

    @app.get("/posts")
    def list_posts():
        posts = Post.query.all()
        return jsonify([p.to_dict() for p in posts]), 200

    @app.post("/posts")
    def create_post():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Missing data"}), 400

        required = ["title", "content", "user_id"]
        if not all(k in data for k in required):
            return jsonify({"error": "title, content, user_id required"}), 400

        # Vérifier que user existe
        user = User.query.get(data["user_id"])
        if not user:
            return jsonify({"error": "user_id does not exist"}), 400

        post = Post(
            title=data["title"],
            content=data["content"],
            user_id=data["user_id"]
        )

        db.session.add(post)
        db.session.commit()

        return jsonify(post.to_dict()), 201

    return app


# Pour pouvoir exécuter python app.py
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
