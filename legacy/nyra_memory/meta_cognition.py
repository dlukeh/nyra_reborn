"""
Meta-Cognition Layer for Nyra (Mini-G5.1)
Strict mode: always ask when uncertain, never silently assume.
"""

from typing import Dict, Any, List


AMBIGUOUS_SINGLE_WORDS = {
    "yes", "yeah", "yep", "ok", "okay", "sure", "fine",
    "do it", "go", "send it", "whatever"
}

PRONOUN_TOKENS = {"this", "that", "it", "those", "these", "there", "here"}


def _is_ambiguous_message(msg: str) -> bool:
    """
    Heuristic ambiguity detector for strict mode.
    We treat messages as ambiguous when they are:
      - extremely short and deictic ("this", "that", "do it")
      - bare confirmations with no explicit referent ("yes", "ok", etc.)
    """
    if not msg:
        return True

    low = msg.lower().strip()

    # Bare confirmations
    if low in AMBIGUOUS_SINGLE_WORDS:
        return True

    # Very short deictic phrases
    tokens = low.split()
    if len(tokens) <= 3 and any(t in PRONOUN_TOKENS for t in tokens):
        return True

    # Vague questions with no object
    if "that thing" in low or "what was i doing" in low:
        return True

    return False


def _check_wm_sanity(wm: Dict[str, Any]) -> Dict[str, bool]:
    flags = {
        "missing_goal": False,
        "missing_behavior_mode": False,
    }
    if not isinstance(wm, dict):
        flags["missing_goal"] = True
        flags["missing_behavior_mode"] = True
        return flags

    if "main_goal" not in wm:
        flags["missing_goal"] = True
    if "behavior_mode" not in wm:
        flags["missing_behavior_mode"] = True

    return flags


def _check_stm_sanity(stm: Dict[str, Any]) -> Dict[str, bool]:
    flags = {
        "stm_inconsistent": False,
    }
    if not isinstance(stm, dict) or not stm:
        return flags

    steps = stm.get("steps") or []
    current = stm.get("current_step")
    if steps:
        # if current_step exists but is out of range or null-like
        if current is not None:
            if isinstance(current, int):
                if current < 1 or current > len(steps):
                    flags["stm_inconsistent"] = True
            elif isinstance(current, str):
                # if it's not one of the step texts
                if not any(current.lower() in str(s).lower() for s in steps):
                    flags["stm_inconsistent"] = True

    return flags


def run_meta_checks(
    wm: Dict[str, Any],
    stm: Dict[str, Any],
    ltm: Dict[str, Any],
    user_message: str,
) -> Dict[str, Any]:
    """
    Core entry point for Nyra's meta-cognition in strict mode.

    Returns a dict:
    {
        "flags": {
            "ambiguous": bool,
            "missing_goal": bool,
            "missing_behavior_mode": bool,
            "stm_inconsistent": bool,
        },
        "notes": [str, ...],
    }
    """
    flags = {
        "ambiguous": False,
        "missing_goal": False,
        "missing_behavior_mode": False,
        "stm_inconsistent": False,
    }
    notes: List[str] = []

    # Ambiguity check
    if _is_ambiguous_message(user_message):
        flags["ambiguous"] = True
        notes.append("User message considered ambiguous under strict mode.")

    # WM sanity
    wm_flags = _check_wm_sanity(wm)
    for k, v in wm_flags.items():
        if v:
            flags[k] = True
            notes.append(f"Working memory issue: {k}")

    # STM sanity
    stm_flags = _check_stm_sanity(stm)
    for k, v in stm_flags.items():
        if v:
            flags[k] = True
            notes.append(f"Short-term memory issue: {k}")

    return {
        "flags": flags,
        "notes": notes,
    }
