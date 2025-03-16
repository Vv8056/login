from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_users():
    with open("users.json", "r") as file:
        return json.load(file)

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

if __name__ == '__main__':
    app.run()