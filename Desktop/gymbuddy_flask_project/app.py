from flask import Flask
from routes.users import users_blueprint
from routes.gym_buddy import gym_buddy_blueprint
from routes.workout_sessions import workout_sessions_blueprint
from routes.workout_plans import workout_plans_blueprint
from routes.notifications import notifications_blueprint

app = Flask(__name__)

# Register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(gym_buddy_blueprint)
app.register_blueprint(workout_sessions_blueprint)
app.register_blueprint(workout_plans_blueprint)
app.register_blueprint(notifications_blueprint)

@app.route('/')
def home():
    return 'GymBuddy Flask App is Running!'

if __name__ == '__main__':
    app.run(debug=True)
