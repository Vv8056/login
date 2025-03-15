from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Allow all origins (Consider restricting this in production)

# Path to JSON file
USER_FILE = "users.json"

# Load users from JSON file
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)["users"]
    return []

# Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    users = load_users()
    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid email or password"}), 401

if _name_ == '_main_':
    app.run(debug=True)
