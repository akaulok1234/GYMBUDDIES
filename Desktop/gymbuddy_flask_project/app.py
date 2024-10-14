from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate('firebase-adminsdk.json')  # Path to your service account key
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

@app.route('/')
def home():
    return 'GymBuddy Flask App is Running!'

# Route to add data
@app.route('/add', methods=['POST'])
def add_data():
    try:
        # Sample data from request
        data = {
            'name': request.json.get('name'),
            'age': request.json.get('age')
        }
        # Add data to Firestore
        db.collection('gymbuddies').add(data)
        return jsonify({'message': 'Data added successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to retrieve data
@app.route('/get', methods=['GET'])
def get_data():
    try:
        gymbuddies_ref = db.collection('gymbuddies')
        docs = gymbuddies_ref.stream()
        
        data_list = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            data_list.append(data)

        return jsonify(data_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
