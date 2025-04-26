from flask import Flask, send_from_directory, abort
from flask_cors import CORS
from backend.models.user import db, User
from backend.routes.auth import auth_bp
from backend.config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    CORS(app, supports_credentials=True)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Serve the static frontend files correctly
    @app.route('/')
    def serve_index():
        return send_from_directory('../frontend', 'index.html')

    @app.route('/<path:filename>')
    def serve_static(filename):
        frontend_path = os.path.join('../frontend', filename)
        if os.path.exists(frontend_path):
            return send_from_directory('../frontend', filename)
        else:
            abort(404)  # Si le fichier n'existe pas => erreur 404

    @app.route('/src/<path:path>')
    def serve_src(path):
        return send_from_directory('../frontend/src', path)

    @app.route('/public/<path:path>')
    def serve_public(path):
        return send_from_directory('../frontend/public', path)

    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
