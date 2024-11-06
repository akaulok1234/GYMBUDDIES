from flask import Blueprint, request, jsonify
from firebase_config import db
import firebase_admin
from firebase_admin import firestore

gym_buddy_blueprint = Blueprint('gym_buddy', __name__)

@gym_buddy_blueprint.route('/add_gym_buddy', methods=['POST'])
def add_gym_buddy():
    """
    Adds a new gym buddy relationship to the 'GymBuddy' collection in Firestore.

    Parameters:
    - user1_id (str): The ID of the first user in the gym buddy relationship.
    - user2_id (str): The ID of the second user in the gym buddy relationship.
    - goals_percentage (float): The percentage of shared goals between the two users.
    - schedule_compatibility (float): The compatibility of their workout schedules.

    Returns:
    - JSON response with a success message and the ID of the newly created gym buddy relationship.
      If an error occurs, a JSON response with an error message is returned.
    """
    try:
        buddy_data = {
            'user1_id': request.json.get('user1_id'),
            'user2_id': request.json.get('user2_id'),
            'goals_percentage': request.json.get('goals_percentage'),
            'schedule_compatibility': request.json.get('schedule_compatibility')
        }
        buddy_ref = db.collection('GymBuddy').add(buddy_data)
        return jsonify({'message': 'Gym buddy relationship added!', 'gym_buddy_id': buddy_ref[1].id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# New Route: Send Gym Buddy Request (with Notification)
@gym_buddy_blueprint.route('/send_gym_buddy_request', methods=['POST'])
def send_gym_buddy_request():
    try:
        user1_id = request.json.get('user1_id')  # Sender
        user2_id = request.json.get('user2_id')  # Receiver
        goals_percentage = request.json.get('goals_percentage')
        schedule_compatibility = request.json.get('schedule_compatibility')

        # Step 1: Create gym buddy relationship
        buddy_data = {
            'user1_id': user1_id,
            'user2_id': user2_id,
            'goals_percentage': goals_percentage,
            'schedule_compatibility': schedule_compatibility
        }
        buddy_ref = db.collection('GymBuddy').add(buddy_data)
        gym_buddy_id = buddy_ref[1].id

        # Step 2: Update both users with the gym buddy reference
        user1_ref = db.collection('Users').document(user1_id)
        user2_ref = db.collection('Users').document(user2_id)

        # Add the gym_buddy_id to each user's workout_buddies list
        user1_ref.update({
            'workout_buddies': firestore.ArrayUnion([gym_buddy_id])
        })
        user2_ref.update({
            'workout_buddies': firestore.ArrayUnion([gym_buddy_id])
        })

        # Step 3: Retrieve Notification Type ID for "Gym Buddy Request"
        notification_type_ref = db.collection('NotificationType').where('type', '==', 'Gym Buddy Request').limit(1).stream()
        notification_type = next(notification_type_ref, None)
        if notification_type is None:
            return jsonify({'error': 'Notification type "Gym Buddy Request" not found'}), 400

        # Step 4: Send Notification to user2_id
        notification_data = {
            'type_id': notification_type.id,
            'user_id': user2_id,  # Receiver of the gym buddy request
            'message': f'{user1_id} sent you a gym buddy request!',
            'date_sent': request.json.get('date_sent')
        }
        db.collection('Notification').add(notification_data)

        return jsonify({
            'message': 'Gym buddy request sent, relationship created, and notification added!',
            'gym_buddy_id': gym_buddy_id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
