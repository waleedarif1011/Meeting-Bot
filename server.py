import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from chatbot.engine import respond

app = Flask(__name__)
CORS(app)

# In-memory session storage
sessions = {}

SAMPLE_TRANSCRIPT = """Meeting: Q4 Planning Session
Date: 2024-01-15
Attendees: Sarah (Product Manager), Mike (Engineer), Lisa (Designer)

Sarah: Let's discuss our Q4 roadmap. We need to prioritize the new user dashboard.
Mike: I can start working on the backend APIs. Should take about 3 weeks.
Lisa: I'll handle the UI mockups. Can have them ready by Friday.
Sarah: Great. Mike, can you also look into the performance issues we discussed?
Mike: Absolutely. I'll investigate the database queries this week.
Lisa: Should we schedule a design review for next Tuesday?
Sarah: Yes, let's do that. I'll send out calendar invites.

Action Items:
- Mike: Develop backend APIs (3 weeks)
- Lisa: Create UI mockups (by Friday)
- Mike: Investigate database performance (this week)
- Sarah: Schedule design review for next Tuesday

Decisions:
- Prioritize the new user dashboard for Q4
- Schedule design review for next Tuesday
"""


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/sample", methods=["GET"])
def sample_transcript():
    return jsonify({"transcript": SAMPLE_TRANSCRIPT}), 200


@app.route("/upload", methods=["POST"])
def upload_transcript():
    data = request.get_json(silent=True) or {}
    transcript = data.get("transcript", "")
    session_id = data.get("session_id", "")

    if not transcript or not session_id:
        return jsonify({"error": "Transcript and session_id are required"}), 400

    sessions[session_id] = {
        "transcript": transcript,
        "chat_history": [],
        "session_id": session_id,
    }

    return jsonify({"message": "Transcript uploaded successfully"}), 200


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    session_id = data.get("session_id", "")

    if not message or not session_id:
        return jsonify({"error": "Message and session_id are required"}), 400

    session_data = sessions.get(session_id)

    if not session_data:
        return jsonify({"error": "Session not found. Please upload a transcript first."}), 404

    session_data["chat_history"].append({"sender": "user", "content": message})
    response_message = respond(message, session_data)
    session_data["chat_history"].append({"sender": "bot", "content": response_message})

    return jsonify({"response": response_message}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
