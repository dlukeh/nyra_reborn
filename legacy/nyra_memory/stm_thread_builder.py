# ============================================
# STM THREAD BUILDER (STRICT MODE) — nyra_memory
# ============================================

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
STM_FILE = BASE_DIR / "stm.json"
STM_MODE = "strict"   # locked default


def _empty_stm():
    return {
        "thread_id": "",
        "steps": [],
        "current_step": 0,
        "mode": STM_MODE,
        "created": "",
        "expires": ""
    }


def load_stm():
    if not STM_FILE.exists():
        return _empty_stm()
    try:
        with STM_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # fallback if corrupted
        return _empty_stm()


def save_stm(data: dict):
    STM_FILE.parent.mkdir(parents=True, exist_ok=True)
    with STM_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def generate_thread_id() -> str:
    return datetime.utcnow().strftime("T-%Y%m%d-%H%M%S")


# ============================================
# CREATE STM THREAD (STRICT MODE)
# ============================================

def create_stm_thread(steps: list) -> dict:
    """
    STRICT MODE:
    - steps must be a list of explicit task strings.
    - no auto-detection, no guessing.
    """
    if not isinstance(steps, list) or not steps:
        return {"error": "Strict mode requires an explicit non-empty list of steps."}

    thread_id = generate_thread_id()

    structured_steps = [
        {"id": i, "task": str(task), "status": "pending"}
        for i, task in enumerate(steps, start=1)
    ]

    stm_data = {
        "thread_id": thread_id,
        "steps": structured_steps,
        "current_step": 1,
        "mode": STM_MODE,
        "created": datetime.utcnow().isoformat(),
        "expires": ""   # to be wired to auto-expire rules later
    }

    save_stm(stm_data)

    return {
        "status": "ok",
        "thread_id": thread_id,
        "steps": steps,
        "message": "STM thread created in nyra_memory/stm.json."
    }


# ============================================
# CLEAR STM
# ============================================

def clear_stm(reason="manual"):
    """
    Wipes the STM file clean.
    """
    empty = _empty_stm()
    save_stm(empty)
    return {"status": "cleared", "reason": reason}


# ============================================
# COMPLETE STEP
# ============================================

def complete_step():
    """
    Marks the current step as completed, advances to the next step,
    and clears STM when the thread is finished.
    """
    data = load_stm()

    # no active thread
    if not data.get("thread_id"):
        return {"error": "No active STM thread."}

    steps = data.get("steps", [])
    current = data.get("current_step", 0)

    # invalid pointer
    if current < 1 or current > len(steps):
        clear_stm(reason="invalid_pointer")
        return {"error": "STM corrupted: pointer out of range. Resetting."}

    # mark step complete
    steps[current - 1]["status"] = "done"

    # next step pointer
    next_step = current + 1

    # THREAD FINISHED
    if next_step > len(steps):
        clear_stm(reason="thread_completed")
        return {
            "status": "done",
            "finished": True,
            "message": "All steps completed. STM cleared."
        }

    # update pointer and save
    data["current_step"] = next_step
    save_stm(data)

    return {
        "status": "ok",
        "finished": False,
        "current_step": next_step,
        "next_task": steps[next_step - 1]["task"],
        "message": "Step completed."
    }
