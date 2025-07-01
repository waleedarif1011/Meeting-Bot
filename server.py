from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot.engine import respond

app = Flask(__name__)
CORS(app)

# In-memory session storage
sessions = {}

@app.route('/upload', methods=['POST'])
def upload_transcript():
    data = request.get_json()
    transcript = data.get('transcript', '')
    session_id = data.get('session_id', '')

    if not transcript or not session_id:
        return jsonify({'error': 'Transcript and session_id are required'}), 400

    # Save to session
    sessions[session_id] = {
        'transcript': transcript,
        'chat_history': []
    }

    return jsonify({'message': 'Transcript uploaded successfully'}), 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    session_id = data.get('session_id', '')

    if not message or not session_id:
        return jsonify({'error': 'Message and session_id are required'}), 400

    session_data = sessions.get(session_id)

    if not session_data:
        return jsonify({'error': 'Session not found. Please upload a transcript first.'}), 404

    # Append to chat history
    chat_entry = {
        'sender': 'user',
        'content': message
    }
    session_data['chat_history'].append(chat_entry)

    # Get response
    response_message = respond(message, session_data)

    # Append bot response to chat history
    chat_entry = {
        'sender': 'bot',
        'content': response_message
    }
    session_data['chat_history'].append(chat_entry)

    return jsonify({'response': response_message}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
