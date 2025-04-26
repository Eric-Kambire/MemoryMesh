from flask import Flask, send_from_directory, abort
from flask_cors import CORS
from backend.models.user import db, User
from backend.routes.auth import auth_bp
from backend.config import Config
import os

# Définir proprement le chemin absolu de ton frontend
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Routes pour servir les fichiers frontend
    @app.route('/')
    def serve_index():
        return send_from_directory(FRONTEND_DIR, 'index.html')

    @app.route('/<path:filename>')
    def serve_static(filename):
        full_path = os.path.join(FRONTEND_DIR, filename)
        if os.path.exists(full_path):
            return send_from_directory(FRONTEND_DIR, filename)
        else:
            abort(404)

    @app.route('/src/<path:path>')
    def serve_src(path):
        return send_from_directory(os.path.join(FRONTEND_DIR, 'src'), path)

    @app.route('/public/<path:path>')
    def serve_public(path):
        return send_from_directory(os.path.join(FRONTEND_DIR, 'public'), path)

    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
