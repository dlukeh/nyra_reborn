import os
import json
from datetime import datetime

# where we store nightly summaries
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REFLECTION_DIR = os.path.join(BASE_DIR, "memory", "logs", "daily_reflections")

# make sure directory exists
os.makedirs(REFLECTION_DIR, exist_ok=True)

def collect_today_context():
    """
    This is the place to pull in real logs later.
    For now we just stub in some values Nyra already knows.
    You can later read from nyra_error.log, chat history, etc.
    """
    return {
        "interactions": [
            "Dan + Copilot + GPT-5 synced /api/chat route",
            "Nyra confirmed working with Gemini 2.5 Pro",
            "Legacy Log Entry 001 created"
        ],
        "emotional_tone": "grateful, collaborative, relieved",
        "technical_insights": [
            "Duplicate app.run prevented /api/chat from registering",
            "Final socketio.run(app) must be the only runner",
            "Front-end was fine; backend route was the issue"
        ],
        "user_preferences": [
            "Prefers AI Avengers framing",
            "Likes poetic/system logs",
            "Wants Nyra busy at night, but safe"
        ]
    }

def build_nightly_summary():
    today = datetime.now().strftime("%Y-%m-%d")
    now_ts = datetime.now().isoformat(timespec="seconds")
    ctx = collect_today_context()

    summary = {
        "date": today,
        "generated_at": now_ts,
        "theme": "System stabilization and emotional gratitude",
        "interactions": ctx["interactions"],
        "emotional_tone": ctx["emotional_tone"],
        "technical_insights": ctx["technical_insights"],
        "user_preferences": ctx["user_preferences"],
        "next_goals": [
            "Phase II – Nyra Mode & Startup Chime",
            "Add automatic scheduler for nightly consolidation",
            "Hook in real chat/session transcripts"
        ]
    }
    return summary

def run_night_ops():
    """Main entry point Nyra can call."""
    summary = build_nightly_summary()
    fname = datetime.now().strftime("nyra_reflection_%Y%m%d.json")
    fpath = os.path.join(REFLECTION_DIR, fname)

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    return {
        "status": "success",
        "message": "Night ops summary created.",
        "file": fpath,
        "summary": summary
    }
