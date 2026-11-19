"""Tests for meeting transcript extraction in chatbot.engine."""

from chatbot.engine import (
    detect_intent,
    extract_action_items,
    extract_decisions,
    extract_participants,
    extract_topics,
    respond,
    summarize_with_textrank,
)

FIXTURE_TRANSCRIPT = """Meeting: Q4 Planning Session
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


def _session(transcript=FIXTURE_TRANSCRIPT):
    return {"transcript": transcript, "chat_history": [], "session_id": "test"}


def test_extract_participants():
    names = extract_participants(FIXTURE_TRANSCRIPT)
    assert "Sarah" in names
    assert "Mike" in names
    assert "Lisa" in names
    assert len(names) == 3


def test_extract_action_items():
    items = extract_action_items(FIXTURE_TRANSCRIPT)
    assert len(items) >= 3
    joined = " ".join(items).lower()
    assert "mike" in joined
    assert "backend" in joined or "apis" in joined
    assert "lisa" in joined


def test_extract_decisions():
    decisions = extract_decisions(FIXTURE_TRANSCRIPT)
    assert len(decisions) >= 1
    joined = " ".join(decisions).lower()
    assert "dashboard" in joined or "design review" in joined or "tuesday" in joined


def test_extract_topics():
    topics = extract_topics(FIXTURE_TRANSCRIPT)
    assert isinstance(topics, list)
    assert len(topics) >= 1


def test_summarize_with_textrank():
    summary = summarize_with_textrank(FIXTURE_TRANSCRIPT)
    assert isinstance(summary, str)
    assert len(summary) > 20


def test_detect_intent():
    assert detect_intent("What were the action items?") == "action_items"
    assert detect_intent("Who participated?") == "participants"
    assert detect_intent("What decisions were made?") == "decisions"
    assert detect_intent("What topics were discussed?") == "topics"
    assert detect_intent("Please summarize the meeting") == "summary"


def test_respond_action_items():
    reply = respond("What were the action items?", _session())
    assert "Action items" in reply or "Mike" in reply
    assert "Lisa" in reply or "Mike" in reply


def test_respond_participants():
    reply = respond("Who participated in this meeting?", _session())
    assert "Sarah" in reply
    assert "Mike" in reply


def test_respond_empty_transcript():
    reply = respond("Summarize", _session(""))
    assert "upload" in reply.lower()
