from flask import Flask, jsonify
from flask_cors import CORS
from routes.user_routes import users_bp
from routes.post_routes import posts_bp

app = Flask(__name__)
CORS(app)

# Register the blueprints
app.register_blueprint(users_bp)
app.register_blueprint(posts_bp)


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the REST API"})


# Production entry point
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
