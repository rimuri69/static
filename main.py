import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows your GUI to connect without CORS blocks

# In-memory database to hold the last received code/message
shared_data = {
    "code": "NONE",
    "message": "No data received yet.",
    "sender": "System"
}

@app.route('/')
def home():
    return jsonify({"status": "API is online", "message": "Go to /data to read/write"}), 200

# This is the endpoint our GUI reads (GET) and writes (POST) to
@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    global shared_data
    if request.method == 'POST':
        try:
            req_data = request.get_json()
            # Update our "database" with the incoming GUI data
            shared_data["code"] = req_data.get("code", "N/A")
            shared_data["message"] = req_data.get("message", "N/A")
            shared_data["sender"] = req_data.get("sender", "N/A")
            
            return jsonify({
                "status": "success",
                "received": shared_data
            }), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
            
    # GET request returns the last saved code
    return jsonify(shared_data), 200

if __name__ == '__main__':
    # Render requires your app to bind to 0.0.0.0 and a dynamic PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
