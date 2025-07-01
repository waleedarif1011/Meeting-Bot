"""
Meeting Bot Engine

This is where candidates implement their AI chatbot logic.
The main function to implement is respond() which takes a user message,
session data, and returns a response.

Session data includes:
- transcript: The uploaded meeting transcript
- chat_history: List of previous messages in the conversation
- session_id: Unique session identifier

Example usage:
    response = respond("What were the main topics discussed?", session_data)
"""


def respond(user_message, session_data):
    """
    Main chatbot response function - IMPLEMENT YOUR AI LOGIC HERE

    Args:
        user_message (str): The user's chat message
        session_data (dict): Session data containing:
            - transcript (str): The uploaded meeting transcript
            - chat_history (list): List of previous messages
            - session_id (str): Unique session identifier

    Returns:
        str: The chatbot's response
    """

    # Extract session data
    transcript = session_data.get("transcript", "")
    chat_history = session_data.get("chat_history", [])
    session_id = session_data.get("session_id", "")

    # PLACEHOLDER IMPLEMENTATION - REPLACE WITH YOUR AI LOGIC

    if not transcript:
        return "Please upload a meeting transcript first so I can help you analyze it."

    # Simple keyword-based responses (replace with your AI implementation)
    return f"Hello! I have access to your meeting transcript ({len(transcript)} characters). What would you like to know about the meeting?"
