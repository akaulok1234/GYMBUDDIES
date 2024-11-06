import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('gymbuddyflaskproject-firebase-adminsdk-d4cng-20be6b7bce.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()
