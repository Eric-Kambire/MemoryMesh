from flask import Flask
from flask_cors import CORS
from backend.models.user import db
from backend.routes.auth import auth_bp
from backend.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
