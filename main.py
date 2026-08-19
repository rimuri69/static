import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store chat history (keeps the last 50 messages in memory)
chat_history = [
    {"sender": "System", "message": "Welcome to the chat room!"}
]

@app.route('/')
def home():
    return jsonify({"status": "Chat API is running"}), 200

@app.route('/data', methods=['GET', 'POST'])
def handle_chat():
    global chat_history
    if request.method == 'POST':
        try:
            req_data = request.get_json()
            sender = req_data.get("sender", "Anonymous").strip()
            message = req_data.get("message", "").strip()
            
            if not message:
                return jsonify({"status": "error", "message": "Message cannot be empty"}), 400
                
            # Add message to history
            new_chat = {"sender": sender, "message": message}
            chat_history.append(new_chat)
            
            # Keep history size manageable (last 50 messages)
            if len(chat_history) > 50:
                chat_history.pop(0)
                
            return jsonify({"status": "success", "sent": new_chat}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
            
    # GET returns the whole history
    return jsonify(chat_history), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
