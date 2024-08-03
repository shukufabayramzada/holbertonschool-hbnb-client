from flask import Flask, request, jsonify, render_template
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
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/place')
def place():
    return render_template('place.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = users.get(email)
        if user and user['password'] == password:
            token = jwt.encode({
                'email': email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'access_token': token})

        return jsonify({'message': 'Invalid credentials'}), 401

    # For GET requests, render the login form
    return render_template('login.html')


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(error=str(e)), 405

if __name__ == '__main__':
    app.run(debug=True)
