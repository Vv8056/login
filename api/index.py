from flask import Flask, request, jsonify
import json
import os

app = Flask(_name_)

# JSON File Path
USER_FILE = "users.json"

# Load users
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

# Save users
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    users = load_users()
    if email in users:
        return jsonify({'error': 'User already exists'}), 400

    users[email] = {"password": password}
    save_users(users)

    return jsonify({'message': 'User registered successfully'}), 200

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    users = load_users()
    if email not in users or users[email]["password"] != password:
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({'message': 'Login successful'}), 200

# Required for Vercel
def handler(event, context):
    return app(event, context)
