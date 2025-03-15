from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import json
import os

app = Flask(_name_)
CORS(app)
bcrypt = Bcrypt(app)

# JSON file to store user data
USER_FILE = "users.json"

# Load users from JSON file
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

# Save users to JSON file
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    users = load_users()
    
    if email in users:
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users[email] = {"password": hashed_password}

    save_users(users)
    return jsonify({'message': 'User registered successfully'}), 200

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    users = load_users()

    if email not in users or not bcrypt.check_password_hash(users[email]["password"], password):
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({'message': 'Login successful'}), 200

# Vercel handler
def handler(event, context):
    return app(event, context)
