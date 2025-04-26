from flask import Blueprint, request, jsonify
from backend.models.user import User, db
from backend.services.jwt_service import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Validate required fields
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Create new user
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    # Generate token
    token = generate_token(user.id)

    return jsonify({
        'message': 'User created successfully',
        'token': token,
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate required fields
    if not all(k in data for k in ['username', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400

    # Find user by username
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Generate token
    token = generate_token(user.id)

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify({'authenticated': False}), 401
    
    token = token.split(' ')[1]
    user_id = verify_token(token)
    
    if not user_id:
        return jsonify({'authenticated': False}), 401
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({'authenticated': False}), 401
        
    return jsonify({
        'authenticated': True,
        'user': user.to_dict()
    }), 200
