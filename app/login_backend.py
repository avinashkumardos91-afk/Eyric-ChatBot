from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy user database
users_db = {
    "admin": "password123",
    "user": "mypassword"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400
    
    username = data['username']
    password = data['password']
    
    if username in users_db and users_db[username] == password:
        return jsonify({
            "message": "Login successful",
            "token": "fake-jwt-token-12345"
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Login API is running. Send a POST request to /login"})

if __name__ == '__main__':
    # Run the server on port 5000
    app.run(host='0.0.0.0', port=5000)
