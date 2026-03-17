# ================================================================
#  LTM CONSOLIDATION MODULE — Mini-G5.1 v1.0
#  Purpose:
#     - Promote important STM items into long-term memory
#     - Enforce rules for what gets saved, summarized, ignored
#     - Provide safe consolidation API for Nyra + app_web
#
#  Author: G5.1 + Danny + copilot
# ================================================================

import json
import os
import time
from datetime import datetime, timedelta

LTM_PATH = os.path.join(os.path.dirname(__file__), "ltm.json")

# ----------------------------------------------------------------
# BASIC LOAD/SAVE
# ----------------------------------------------------------------
def load_ltm():
    if not os.path.exists(LTM_PATH):
        return {}
    try:
        with open(LTM_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_ltm(data: dict):
    with open(LTM_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ----------------------------------------------------------------
# CONSOLIDATION RULESET
# ----------------------------------------------------------------
CONSOLIDATION_RULES = {
    "promote_if_done": True,            # If STM thread completed → promote summary
    "promote_threshold": 2,             # Minimum thread length to promote
    "never_save_phrases": [
        "sensitive",
        "temporary",
        "debug",
        "ignore"
    ],
    "summaries_only": True,             # Save short summary instead of full detail
}

# ----------------------------------------------------------------
# UTILITIES
# ----------------------------------------------------------------
def contains_blocked_phrase(text: str):
    text = text.lower()
    for phrase in CONSOLIDATION_RULES["never_save_phrases"]:
        if phrase in text:
            return True
    return False

def summarize_thread(stm: dict):
    """
    Convert STM thread into a short human-readable summary.
    """
    steps = stm.get("steps", [])
    summary_lines = []

    for step in steps:
        txt = step.get("text") or step.get("task") or "Unknown step"
        summary_lines.append(txt)

    return "; ".join(summary_lines)

# ----------------------------------------------------------------
# CONSOLIDATION MAIN PIPELINE
# ----------------------------------------------------------------
def consolidate_stm_to_ltm(stm: dict):
    """
    Promote an STM thread into LTM if rules approve.
    Returns:
        {
            "status": "promoted" | "ignored" | "blocked",
            "message": "...",
            "ltm_key": optional
        }
    """
    if not stm or not stm.get("steps"):
        return {"status": "ignored", "message": "No STM thread to consolidate."}

    steps = stm["steps"]
    thread_text = " ".join([s.get("text","") for s in steps])

    # 1. Blocklist check
    if contains_blocked_phrase(thread_text):
        return {"status": "blocked", "message": "Contains blocked phrase. Not saved."}

    # 2. Minimum length threshold
    if len(steps) < CONSOLIDATION_RULES["promote_threshold"]:
        return {"status": "ignored", "message": "Thread too short to promote."}

    # 3. Build summary or full thread
    if CONSOLIDATION_RULES["summaries_only"]:
        entry = summarize_thread(stm)
    else:
        entry = stm

    # 4. Insert into LTM file
    ltm = load_ltm()
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    key = f"stm_{timestamp}"
    ltm[key] = entry
    save_ltm(ltm)

    return {"status": "promoted", "message": "STM promoted to LTM.", "ltm_key": key}
