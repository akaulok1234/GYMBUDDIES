from flask import Blueprint, request, jsonify
from firebase_config import db

workout_sessions_blueprint = Blueprint('workout_sessions', __name__)

@workout_sessions_blueprint.route('/schedule_workout_session', methods=['POST'])
def schedule_workout_session():
    try:
        session_data = {
            'gym_buddy': request.json.get('gym_buddy'),
            'workout_type': request.json.get('workout_type'),
            'duration': request.json.get('duration'),
            'calories_burned': request.json.get('calories_burned'),
            'date': request.json.get('date'),
            'time': request.json.get('time'),
            'location': request.json.get('location')
        }
        session_ref = db.collection('WorkoutSessions').add(session_data)
        return jsonify({'message': 'Workout session scheduled!', 'session_id': session_ref[1].id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@workout_sessions_blueprint.route('/get_all_workout_sessions', methods=['GET'])
def get_all_workout_sessions():
    try:
        sessions_ref = db.collection('WorkoutSessions')
        sessions = sessions_ref.stream()
        session_list = [{**session.to_dict(), 'id': session.id} for session in sessions]
        return jsonify(session_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
