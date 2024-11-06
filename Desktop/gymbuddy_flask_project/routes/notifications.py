from flask import Blueprint, request, jsonify
from firebase_config import db

notifications_blueprint = Blueprint('notifications', __name__)

@notifications_blueprint.route('/add_notification_type', methods=['POST'])
def add_notification_type():
    try:
        notification_type_data = {
            'type': request.json.get('type')
        }
        type_ref = db.collection('NotificationType').add(notification_type_data)
        return jsonify({'message': 'Notification type added successfully!', 'type_id': type_ref[1].id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notifications_blueprint.route('/add_notification', methods=['POST'])
def add_notification():
    try:
        notification_data = {
            'type_id': request.json.get('type_id'),
            'user_id': request.json.get('user_id'),
            'message': request.json.get('message'),
            'date_sent': request.json.get('date_sent')
        }
        notification_ref = db.collection('Notification').add(notification_data)
        return jsonify({'message': 'Notification added successfully!', 'notification_id': notification_ref[1].id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
