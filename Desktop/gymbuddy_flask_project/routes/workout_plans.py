from flask import Blueprint, request, jsonify
from firebase_config import db

workout_plans_blueprint = Blueprint('workout_plans', __name__)

@workout_plans_blueprint.route('/add_workout_plan', methods=['POST'])
def add_workout_plan():
    try:
        plan_data = {
            'plan_name': request.json.get('plan_name'),
            'difficulty': request.json.get('difficulty'),
            'steps': request.json.get('steps'),
            'estimated_duration': request.json.get('estimated_duration'),
            'target_muscle_groups': request.json.get('target_muscle_groups'),
            'session_id': request.json.get('session_id')
        }
        plan_ref = db.collection('WorkoutPlans').add(plan_data)
        return jsonify({'message': 'Workout plan added to session!', 'plan_id': plan_ref[1].id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@workout_plans_blueprint.route('/get_all_workout_plans', methods=['GET'])
def get_all_workout_plans():
    try:
        plans_ref = db.collection('WorkoutPlans')
        plans = plans_ref.stream()
        plan_list = [{**plan.to_dict(), 'id': plan.id} for plan in plans]
        return jsonify(plan_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
