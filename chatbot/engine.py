"""
Implemented features:
- Real topic extraction
- Accurate decisions & action items
- Robust, clean responses for all major queries
- Added TextRank summarization using Sumy
"""

import re
from collections import Counter
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer

# --- PARTICIPANT EXTRACTION ---
def get_participant_names(transcript):
    """
    Extracts a set of participant names from the transcript.
    Looks for an 'Attendees:' line, or falls back to speaker labels (e.g., 'Mike:').
    Returns a set of lowercase names.
    """
    m = re.search(r"Attendees?:\s*(.*)", transcript, re.IGNORECASE)
    if m:
        attendees = m.group(1)
        # Remove anything in parentheses (roles), strip spaces, lowercase
        names = [re.sub(r"\s*\(.*?\)", "", n).strip().lower() for n in attendees.split(',')]
        return set([n for n in names if n])
    # Fallback: find all lines like 'Name:'
    names = set()
    for line in transcript.splitlines():
        m = re.match(r"([A-Z][a-z]+):", line)
        if m:
            names.add(m.group(1).lower())
    return names

def extract_participants(transcript):
    """
    Returns a sorted, capitalized list of unique participant names for display.
    """
    names = get_participant_names(transcript)
    if names:
        return [n.capitalize() for n in sorted(names)]
    return []

# --- TOPIC EXTRACTION ---
def extract_topics(transcript, top_n=5):
    """
    Returns a list of key topics discussed in the meeting.
    First, looks for an explicit 'Agenda' or 'Topics' section.
    If not found, uses most common non-name words (likely nouns) as topics.
    """
    # Check for explicit 'Agenda' or 'Topics' section
    explicit = re.findall(r"(?:Agenda|Topics?):\s*(.*)", transcript, re.I)
    if explicit:
        all_topics = []
        for line in explicit:
            topics = re.split(r'[,.]', line)
            all_topics.extend([t.strip() for t in topics if t.strip()])
        return all_topics[:top_n]

    # Otherwise, use word frequency (excluding names and common words)
    names = get_participant_names(transcript)
    word_counter = Counter()
    for line in transcript.splitlines():
        # Remove timestamps and speaker names
        line = re.sub(r"^\d{1,2}:\d{2}(?: [AP]M)?:\s*", "", line)
        line = re.sub(r"([A-Z][a-z]+):", "", line)
        words = re.findall(r'\b([a-z]{3,})\b', line.lower())
        for w in words:
            if w not in names and w not in {
                'will','can','should','need','want','have','this','that','from',
                'with','for','the','and','but','are','was','our','has','you',
                'about','let','all','any','more','your','now','just','not',
                'okay','done','like','when','who','time','yes','no','got'
            } and len(w) > 3:
                word_counter[w] += 1
    topics = [w for w, c in word_counter.most_common(top_n)]
    return topics

# --- ACTION ITEM EXTRACTION ---
def extract_action_items(transcript):
    """
    Extracts action items from the transcript.
    Looks for an explicit 'Action Items:' section, or infers from statements like 'I will...'.
    Returns a list of action item strings.
    """
    action_items = []
    # Check for explicit 'Action Items:' section
    ai_section = re.search(r"(Action Items:.*?)(\n\S|\Z)", transcript, re.DOTALL | re.IGNORECASE)
    if ai_section:
        lines = re.findall(r"-\s*([A-Za-z]+):\s*(.*)", ai_section.group(1))
        for name, task in lines:
            action_items.append(f"{name.strip()}: {task.strip()}")
        if action_items:
            return action_items

    # Otherwise, infer from dialogue (look for commitments)
    for line in transcript.splitlines():
        m = re.match(r"([A-Z][a-z]+):\s*(.*)", line)
        if m:
            name, statement = m.groups()
            # Look for phrases indicating a promise or commitment
            if re.search(
                r"\b(i ?('| wi)?ll|i can|i should|i need to|i'll|i'll try|i can|let's|we need to|i'll handle|i'll send|i'll schedule|i'll take care)\b",
                statement, re.I
            ):
                # Exclude questions and very short statements
                if not statement.strip().endswith('?') and len(statement.strip().split()) > 2:
                    action_items.append(f"{name}: {statement.strip()}")
    return action_items

# --- DECISION EXTRACTION ---
def extract_decisions(transcript):
    """
    Extracts decisions made in the meeting.
    Looks for an explicit 'Decisions:' section, or lines with decision-related keywords.
    Returns a list of decision strings.
    """
    # Check for explicit 'Decisions' section
    m = re.search(r"Decisions?:\s*(.*?)(\n\S|\Z)", transcript, re.DOTALL | re.I)
    if m:
        section = m.group(1)
        return [line.strip('- ').strip() for line in section.split('\n') if line.strip()]
    # Otherwise, look for decision-like lines
    decisions = []
    for line in transcript.splitlines():
        # Look for strong decision keywords
        if re.search(
            r"\b(decided|agreed|approved|will be|let's|will proceed|resolution|move forward|schedule|assign|finalize|confirm|deadline|approved)\b",
            line, re.I
        ):
            # Filter out questions
            if not line.strip().endswith('?'):
                # Remove timestamps and names
                clean = re.sub(r"^\d{1,2}:\d{2}(?: [AP]M)?:\s*", "", line)
                clean = re.sub(r"^[A-Z][a-z]+:", "", clean).strip()
                if clean and len(clean.split()) > 3:
                    decisions.append(clean)
    return decisions

# --- MEETING SUMMARY ---
def summarize_meeting(transcript):
    """
    Produces a concise meeting summary by combining intro, topics, decisions, and action items.
    Returns a multi-line summary string.
    """
    lines = [l.strip() for l in transcript.splitlines() if l.strip()]
    summary = []

    # Add first statement/meeting intro
    if lines:
        summary.append(f"Summary: {lines[0]}")

    # Topics
    topics = extract_topics(transcript, 3)
    if topics:
        summary.append("Main topics: " + ', '.join(topics))

    # Key decisions
    decs = extract_decisions(transcript)
    if decs:
        summary.append("Key decisions made:")
        for d in decs[:4]:
            summary.append(f"- {d}")

    # Action items
    actions = extract_action_items(transcript)
    if actions:
        summary.append("Action items:")
        for a in actions[:4]:
            summary.append(f"- {a}")

    # Add ending (optional)
    if len(lines) > 3:
        summary.append(f"Closing: {lines[-1]}")

    return '\n'.join(summary)

# --- TEXTRANK SUMMARIZATION ---
def summarize_with_textrank(transcript, top_n=3):
    """
    Summarizes the transcript using the TextRank algorithm (from the Sumy library).
    Returns a short summary string with the top N sentences.
    """
    parser = PlaintextParser.from_string(transcript, PlaintextParser.from_string(transcript, PlaintextParser.from_string))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, top_n)
    return ' '.join([str(sentence) for sentence in summary])

# --- INTENT DETECTION ---
def detect_intent(user_message):
    """
    Determines what the user is asking for (intent).
    Returns one of: action_items, participants, decisions, topics, summary, followup
    """
    msg = user_message.lower()
    if any(x in msg for x in ["action items", "tasks assigned", "who will", "who needs to", "todo", "to do", "responsibilities", "deliverables"]):
        return "action_items"
    if any(x in msg for x in ["participants", "attendees", "who was in", "who attended", "who joined", "who were present", "who participated"]):
        return "participants"
    if any(x in msg for x in ["decisions", "what was decided", "agreements", "agreed", "resolution", "outcome", "conclusion"]):
        return "decisions"
    if any(x in msg for x in ["topic", "discussed", "agenda", "subject", "what did you talk", "what was the meeting about"]):
        return "topics"
    if any(x in msg for x in ["summarize", "summary", "brief", "recap", "overall", "main points", "key points"]):
        return "summary"
    # Fallback
    return "followup"

# --- FOLLOW-UP HANDLING ---
def handle_followup(user_message, transcript, chat_history):
    """
    Handles follow-up questions, such as asking about a specific person's tasks or decisions.
    Looks for a name in the user message and returns related action items or decisions.
    """
    m = re.search(r'\b([A-Z][a-z]+)\b', user_message)
    if m:
        name = m.group(1)
        # Search for action items or decisions about this person
        items = [item for item in extract_action_items(transcript) if name.lower() in item.lower()]
        if items:
            return f"Here are the tasks assigned to {name}:\n" + "\n".join(f"- {i}" for i in items)
        # Search for decisions mentioning this person
        decs = [d for d in extract_decisions(transcript) if name.lower() in d.lower()]
        if decs:
            return f"Here are decisions involving {name}:\n" + "\n".join(f"- {d}" for d in decs)
    return "Could you clarify your question? I can help with action items, participants, decisions, topics, or summaries."

# --- MAIN CHATBOT RESPONSE FUNCTION ---
def respond(user_message, session_data):
    """
    Main chatbot response function.
    This is the entry point called by the Flask server.

    Args:
        user_message (str): The user's chat message
        session_data (dict): Session data containing:
            - transcript (str): The uploaded meeting transcript
            - chat_history (list): List of previous messages
            - session_id (str): Unique session identifier

    Returns:
        str: The chatbot's response
    """

    transcript = session_data.get("transcript", "")
    chat_history = session_data.get("chat_history", [])
    session_id = session_data.get("session_id", "")

    if not transcript.strip():
        return "Please upload a meeting transcript first so I can assist you."

    # Detect intent (what the user wants)
    intent = detect_intent(user_message)

    if intent == "participants":
        names = extract_participants(transcript)
        if names:
            return "Participants in this meeting:\n" + "\n".join(f"- {n}" for n in names)
        else:
            return "Sorry, I couldn't find a clear list of participants."
    elif intent == "action_items":
        items = extract_action_items(transcript)
        if items:
            return "Action items:\n" + "\n".join(f"- {i}" for i in items)
        else:
            return "No action items were found in this transcript."
    elif intent == "decisions":
        decs = extract_decisions(transcript)
        if decs:
            return "Key decisions made:\n" + "\n".join(f"- {d}" for d in decs)
        else:
            return "No specific decisions were found in this transcript."
    elif intent == "topics":
        topics = extract_topics(transcript, 5)
        if topics:
            return "Main topics discussed:\n" + ", ".join(topics)
        else:
            return "I couldn't determine the main topics."
    elif intent == "summary":
        # Use TextRank for summary if asked
        summary = summarize_with_textrank(transcript)
        return summary
    elif intent == "followup":
        return handle_followup(user_message, transcript, chat_history)

    return "I'm here to help you with meeting summaries, action items, participants, decisions, or topics. Please clarify your request."
