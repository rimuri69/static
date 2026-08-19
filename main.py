import os
import hashlib
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory database (resets when server restarts)
users = {}          # { "username": "hashed_password" }
chat_history = []   # [ {"sender": "System", "message": "Global chat initialized."} ]
private_messages = [] # [ {"sender": "A", "receiver": "B", "message": "Hi"} ]

def hash_password(password):
    """Simple SHA-256 password hashing for demonstration."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@app.route('/')
def home():
    return jsonify({"status": "Auth & DM Chat Server Online"}), 200

# --- AUTHENTICATION ROUTES ---

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get("username", "").strip().lower()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password required."}), 400
    if username in users:
        return jsonify({"status": "error", "message": "Username already exists."}), 400

    users[username] = hash_password(password)
    return jsonify({"status": "success", "message": "Account created successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip().lower()
    password = data.get("password", "").strip()

    if username not in users or users[username] != hash_password(password):
        return jsonify({"status": "error", "message": "Invalid username or password."}), 401

    return jsonify({"status": "success", "message": "Logged in successfully!", "username": username}), 200

@app.route('/users', methods=['GET'])
def get_users():
    """Returns a list of all registered users so clients can start DMs."""
    return jsonify(list(users.keys())), 200

# --- CHAT & DM ROUTES ---

@app.route('/data', methods=['GET', 'POST'])
def handle_global_chat():
    global chat_history
    if request.method == 'POST':
        data = request.get_json() or {}
        sender = data.get("sender", "Anonymous")
        message = data.get("message", "").strip()
        if message:
            chat_history.append({"sender": sender, "message": message})
            if len(chat_history) > 50:
                chat_history.pop(0)
            return jsonify({"status": "success"}), 201
    return jsonify(chat_history), 200

@app.route('/dm', methods=['GET', 'POST'])
def handle_dms():
    global private_messages
    if request.method == 'POST':
        data = request.get_json() or {}
        sender = data.get("sender", "").strip().lower()
        receiver = data.get("receiver", "").strip().lower()
        message = data.get("message", "").strip()

        if sender and receiver and message:
            private_messages.append({"sender": sender, "receiver": receiver, "message": message})
            return jsonify({"status": "success"}), 201
        return jsonify({"status": "error", "message": "Invalid payload"}), 400

    # GET requests fetch messages belonging only to the sender/receiver pair
    sender = request.args.get("sender", "").strip().lower()
    receiver = request.args.get("receiver", "").strip().lower()

    filtered_dms = [
        msg for msg in private_messages
        if (msg["sender"] == sender and msg["receiver"] == receiver) or
           (msg["sender"] == receiver and msg["receiver"] == sender)
    ]
    return jsonify(filtered_dms), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
