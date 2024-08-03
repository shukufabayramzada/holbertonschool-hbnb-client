from flask import Flask, request, jsonify
import jwt
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'

users = {
    "user@example.com": {
        "password": "password123",
        "name": "John Doe"
    },
    "hello@example.com": {
        "password": "password123!",
        "name": "John Wor"
    }
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    print(f"Received login attempt for email: {email}")

    user = users.get(email)
    if user and user['password'] == password:
        token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        print(f"Login successful for email: {email}")
        print(f"Generated token: {token}")

        return jsonify({'access_token': token})

    print("Login failed: Invalid credentials")
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
