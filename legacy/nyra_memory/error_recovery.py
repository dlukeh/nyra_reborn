"""
ERROR RECOVERY & SAFE MODE TRAY — Mini-G5.1
-------------------------------------------------------
Provides:
- Startup self-check diagnostics
- JSON file validation
- Missing/corrupt memory file reconstruction
- Safe Mode activation + exit
- Health status reporting

Designed for integration with:
- memory_manager.py
- meta_cognition.py
- app_web.py (boot hook + commands)
"""

import json
import os
from typing import Dict, Any


# ============================================================
#                   INTERNAL HELPERS
# ============================================================

def _load_json_safe(path: str) -> Any:
    """Attempt to load JSON; return None if invalid or unreadable."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _write_json(path: str, data: Dict[str, Any]) -> None:
    """Safe writer used for rebuilding memory files."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        raise RuntimeError(f"Failed writing JSON to {path}: {e}")


# ============================================================
#                DEFAULT MEMORY TEMPLATES
# ============================================================

DEFAULT_WM = {
    "main_goal": "stabilize your memory system",
    "behavior_mode": "direct_blade"
}

DEFAULT_STM = {
    # empty until user creates a thread
}

DEFAULT_LTM = {
    # empty until consolidation generates entries
}


# ============================================================
#                SAFE MODE STATE (stored in WM)
# ============================================================

def enter_safe_mode(wm: Dict[str, Any], save_func) -> Dict[str, Any]:
    """
    Activate Safe Mode:
    - restrict behavior
    - suppress unnecessary features
    - require explicit commands
    """
    wm["safe_mode"] = True
    save_func(wm)
    return wm


def exit_safe_mode(wm: Dict[str, Any], save_func) -> Dict[str, Any]:
    """Deactivate Safe Mode and restore normal behavior."""
    wm["safe_mode"] = False
    save_func(wm)
    return wm


# ============================================================
#                    DIAGNOSTIC ENGINE
# ============================================================

def run_startup_self_check(memory_paths: Dict[str, str]) -> Dict[str, Any]:
    """
    Perform boot-level diagnostics on:
    - wm.json
    - stm.json
    - ltm.json
    - logs folder
    """

    results = {
        "wm_status": "ok",
        "stm_status": "ok",
        "ltm_status": "ok",
        "logs_status": "ok",
        "repairs": []
    }

    # ------ WM CHECK ------
    wm_raw = _load_json_safe(memory_paths["wm"])
    if wm_raw is None or not isinstance(wm_raw, dict):
        _write_json(memory_paths["wm"], DEFAULT_WM)
        results["wm_status"] = "repaired"
        results["repairs"].append("wm.json rebuilt")

    # ------ STM CHECK ------
    stm_raw = _load_json_safe(memory_paths["stm"])
    if stm_raw is None or not isinstance(stm_raw, dict):
        _write_json(memory_paths["stm"], DEFAULT_STM)
        results["stm_status"] = "repaired"
        results["repairs"].append("stm.json rebuilt")

    # ------ LTM CHECK ------
    ltm_raw = _load_json_safe(memory_paths["ltm"])
    if ltm_raw is None or not isinstance(ltm_raw, dict):
        _write_json(memory_paths["ltm"], DEFAULT_LTM)
        results["ltm_status"] = "repaired"
        results["repairs"].append("ltm.json rebuilt")

    # ------ LOGS FOLDER CHECK ------
    logs_path = memory_paths["logs"]
    if not os.path.exists(logs_path):
        try:
            os.makedirs(logs_path, exist_ok=True)
            results["logs_status"] = "repaired"
            results["repairs"].append("logs folder created")
        except Exception:
            results["logs_status"] = "error"

    return results


# ============================================================
#                    STATUS REPORTING
# ============================================================

def health_report(result_dict: Dict[str, Any]) -> str:
    """
    Produce a readable diagnostic summary.
    Used by:
    - boot logs
    - `diagnose` command
    """
    rep = result_dict.get("repairs", [])
    rep_str = ", ".join(rep) if rep else "none"

    return (
        "SYSTEM HEALTH REPORT\n"
        "---------------------\n"
        f"WM:   {result_dict.get('wm_status')}\n"
        f"STM:  {result_dict.get('stm_status')}\n"
        f"LTM:  {result_dict.get('ltm_status')}\n"
        f"Logs: {result_dict.get('logs_status')}\n"
        f"Repairs: {rep_str}\n"
    )
