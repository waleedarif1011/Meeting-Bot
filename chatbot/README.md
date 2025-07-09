# Meeting Bot - Chatbot Engine

This document explains the **chatbot engine** for the Meeting Bot. The engine analyzes uploaded meeting transcripts and answers user questions about the meeting, such as participants, topics, action items, decisions, and summaries.

---

## What Does this Do?

- **Extracts Participants:** Finds out who attended the meeting.
- **Finds Action Items:** Lists tasks or responsibilities assigned during the meeting.
- **Identifies Decisions:** Shows what was decided or agreed upon.
- **Detects Topics:** Lists the main topics discussed.
- **Summarizes Meetings:** Gives a short summary using the TextRank algorithm.
- **Handles Follow-up Questions:** Answers follow-up questions about people or topics.

---

## How Does It Work?

The engine uses regular expressions, word counting, and the Sumy TextRank algorithm to analyze transcripts. It is designed to be robust and easy to understand.

### Main Functions (with Simple Explanations)

#### 1. `get_participant_names(transcript)`
- **Purpose:** Finds participant names from an "Attendees:" line or from speaker labels (like "Mike:").
- **Returns:** A set of lowercase names.

#### 2. `extract_participants(transcript)`
- **Purpose:** Returns a sorted, capitalized list of unique participant names for display.

#### 3. `extract_topics(transcript, top_n=5)`
- **Purpose:** Lists the main topics discussed.
- **How:** Looks for an explicit "Agenda" or "Topics" section. If not found, uses the most common non-name words as topics.

#### 4. `extract_action_items(transcript)`
- **Purpose:** Finds action items (tasks or commitments).
- **How:** Looks for an explicit "Action Items:" section, or infers from statements like "I will..." or "I'll handle...".

#### 5. `extract_decisions(transcript)`
- **Purpose:** Finds decisions made in the meeting.
- **How:** Looks for an explicit "Decisions:" section, or lines with decision-related keywords (like "decided", "agreed").

#### 6. `summarize_meeting(transcript)`
- **Purpose:** Creates a concise summary of the meeting, including intro, topics, decisions, and action items.

#### 7. `summarize_with_textrank(transcript, top_n=3)`
- **Purpose:** Uses the TextRank algorithm (from the Sumy library) to generate a short summary with the top N sentences.

#### 8. `detect_intent(user_message)`
- **Purpose:** Figures out what the user is asking for (e.g., action items, participants, decisions, topics, summary, or a follow-up).

#### 9. `handle_followup(user_message, transcript, chat_history)`
- **Purpose:** Handles follow-up questions, such as asking about a specific person's tasks or decisions.

#### 10. `respond(user_message, session_data)`
- **Purpose:** Main function called by the server. Detects user intent and returns the appropriate answer using the above functions.

---

## Dependencies

- **Sumy**: For TextRank summarization.
- **re**: For regular expression-based text extraction.
- **collections.Counter**: For counting word occurrences.

---

## Example Usage

1. **Upload a Transcript:**
   - The transcript is stored in the session.
2. **Ask Questions:**
   - Examples:
     - "Who participated in the meeting?"
     - "What were the main topics discussed?"
     - "What action items were assigned?"
     - "Summarize the meeting."
3. **Get Answers:**
   - The engine analyzes the transcript and returns clear, relevant answers.

---

## Reusability

- All functions are commented with simple explanations.
- The code is organized by feature (participants, topics, action items, decisions, summary, intent detection, follow-up, main response).
- Easy to read, modify, and extend.

---

## See Also
- [../README.md](../README.md) — Main project overview
- [../server.py](../server.py) — Flask server that calls this engine
- [requirements.txt](../requirements.txt) — Python dependencies
