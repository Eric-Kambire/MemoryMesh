from functools import wraps
from flask import request, jsonify
from backend.services.jwt_service import verify_token

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        user_id = verify_token(token)
        if not user_id:
            return jsonify({'message': 'Invalid or expired token'}), 401

        # Add user_id to kwargs so the route can use it
        kwargs['user_id'] = user_id
        return f(*args, **kwargs)

    return decorated_function
