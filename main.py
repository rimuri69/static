import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# App Metadata & Update Info
APP_METADATA = {
    "latest_version": "2.0.0",
    "download_url": "https://github.com/yourusername/your-repo/releases",  # Replace with your safe download host
    "update_notes": "New neon styling and performance optimizations!"
}

chat_history = [
    {"sender": "[SYSTEM]", "message": "CyberChat Mainframe Online. Keep it lit."}
]

@app.route('/')
def home():
    return jsonify({"status": "CyberChat API Running"}), 200

# Endpoint to fetch chat history AND update metadata
@app.route('/data', methods=['GET', 'POST'])
def handle_chat():
    global chat_history
    if request.method == 'POST':
        try:
            req_data = request.get_json()
            sender = req_data.get("sender", "NetRunner").strip()
            message = req_data.get("message", "").strip()
            
            if not message:
                return jsonify({"status": "error", "message": "Void messages rejected."}), 400
                
            new_chat = {"sender": sender, "message": message}
            chat_history.append(new_chat)
            
            if len(chat_history) > 50:
                chat_history.pop(0)
                
            return jsonify({"status": "success", "sent": new_chat}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
            
    # GET returns both history and version info
    return jsonify({
        "history": chat_history,
        "update_info": APP_METADATA
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
