from flask import Blueprint, request, jsonify
from firebase_config import db

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/add_user', methods=['POST'])
def add_user():
    try:
        user_data = {
            'first_name': request.json.get('first_name'),
            'last_name': request.json.get('last_name'),
            'age': request.json.get('age'),
            'email': request.json.get('email'),
            'goals': request.json.get('goals'),
            'fitness_level': request.json.get('fitness_level'),
            'schedule': request.json.get('schedule'),
            'workout_buddies': []  # Initialize workout_buddies as an empty array
        }
        user_ref = db.collection('Users').add(user_data)
        return jsonify({'message': 'User added successfully!', 'user_id': user_ref[1].id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_blueprint.route('/get_all_users', methods=['GET'])
def get_all_users():
    try:
        users_ref = db.collection('Users')
        users = users_ref.stream()
        user_list = [{**user.to_dict(), 'id': user.id} for user in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
