from flask import Flask, jsonify
from flask_cors import CORS
from users import users_bp
from posts import posts_bp

app = Flask(__name__)
CORS(app)

# Register the blueprints
app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the REST API"})


if __name__ == '__main__':
    app.run(debug=True)
