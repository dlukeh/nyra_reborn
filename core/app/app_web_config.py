# =====================================================
#   app_web_config.py — Config-Driven Dual-Agent Server
#   - Separate from legacy Nyra (app_web.py)
#   - Fully config-driven
#   - Memory support included
#   - Behavior modes included
#   - Advanced memory commands (human-only)
# =====================================================

import os
import json
import argparse
from flask import Flask, request, jsonify
from openai import OpenAI

# -----------------------------------------------------
# Memory System
# -----------------------------------------------------
from memory_manager import MemoryManager

# -----------------------------------------------------
# Behavior Mode Engine
# -----------------------------------------------------
def apply_behavior_mode(text: str, mode: str) -> str:
    """
    Adjust output tone based on the selected behavior mode.
    Tone only — does not alter meaning.
    """
    return text.strip()  # behavior modes can be expanded later


# -----------------------------------------------------
# Paths / Flask Setup
# -----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

app = Flask(__name__)

# Globals set at startup
CONFIG = {}
SYSTEM_PROMPT = ""
MEMORY: MemoryManager | None = None  # type: ignore

# Single OpenAI Client (uses OPENAI_API_KEY)
client = OpenAI()


# -----------------------------------------------------
# Config Loading
# -----------------------------------------------------
def load_config(config_path: str) -> dict:
    """
    Load a JSON config file.
    """

    if not os.path.isabs(config_path):
        config_path = os.path.join(ROOT_DIR, config_path)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    required = ["agent_name", "model", "system_prompt_path", "memory_dir"]
    for r in required:
        if r not in data:
            raise ValueError(f"Missing required config key: {r}")

    return data


def load_system_prompt(path: str) -> str:
    """
    Load system prompt.
    """

    if not os.path.isabs(path):
        path = os.path.join(ROOT_DIR, path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"System prompt not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# -----------------------------------------------------
# ROUTES
# -----------------------------------------------------
@app.route("/", methods=["GET"])
def root():
    """
    Basic health/status info.
    """
    return jsonify({
        "status": "online",
        "agent": CONFIG.get("agent_name"),
        "model": CONFIG.get("model"),
        "behavior_mode": CONFIG.get("personality_mode"),
        "memory_dir": CONFIG.get("memory_dir"),
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Chat endpoint with memory + behavior modes.
    """
    global MEMORY

    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Missing 'message'"}), 400

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    # -----------------------------------------------------
    # FIXED: Modern GPT-5.1 token parameter:
    #         max_completion_tokens   ✔ (correct)
    # -----------------------------------------------------
    try:
        response = client.chat.completions.create(
            model=CONFIG["model"],
            messages=messages,
            max_completion_tokens=2048,
            temperature=CONFIG.get("temperature", 0.6)
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    reply = response.choices[0].message.content

    # Apply behavior mode
    behavior_mode = CONFIG.get("personality_mode", "direct_blade")
    reply = apply_behavior_mode(reply, behavior_mode)

    # Log memory (non-fatal on error)
    try:
        if MEMORY is not None:
            MEMORY.log_interaction(user_message, reply)
    except Exception as e:
        print("[WARNING] Memory logging failed:", e)

    return jsonify({"response": reply})


# -----------------------------------------------------
# Memory Snapshot Endpoints
# -----------------------------------------------------
@app.route("/api/memory/wm", methods=["GET"])
def memory_wm():
    try:
        if MEMORY is None:
            return jsonify({"error": "Memory system not initialized"}), 500
        return jsonify(MEMORY.get_wm_snapshot())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/memory/stm", methods=["GET"])
def memory_stm():
    try:
        if MEMORY is None:
            return jsonify({"error": "Memory system not initialized"}), 500
        return jsonify(MEMORY.get_stm_snapshot())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/memory/ltm", methods=["GET"])
def memory_ltm():
    try:
        if MEMORY is None:
            return jsonify({"error": "Memory system not initialized"}), 500
        return jsonify(MEMORY.get_ltm_snapshot())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------
# Advanced Memory Command Endpoints (Human-Only)
# -----------------------------------------------------
@app.route("/api/memory/write", methods=["POST"])
def memory_write():
    global MEMORY

    if MEMORY is None:
        return jsonify({"error": "Memory system not initialized"}), 500

    data = request.get_json(silent=True) or {}
    tier = (data.get("tier") or "").lower().strip()
    text = (data.get("data") or data.get("text") or "").strip()
    meta = data.get("meta") or {}

    if tier not in ("wm", "stm", "ltm"):
        return jsonify({"error": "Invalid or missing 'tier'. Use wm, stm, or ltm."}), 400

    if not text:
        return jsonify({"error": "Missing 'data' (or 'text') field"}), 400

    try:
        entry = MEMORY.write_memory(tier=tier, text=text, meta=meta)
        return jsonify({"status": "success", "entry": entry})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/memory/promote", methods=["POST"])
def memory_promote():
    global MEMORY

    if MEMORY is None:
        return jsonify({"error": "Memory system not initialized"}), 500

    data = request.get_json(silent=True) or {}
    stm_id = (data.get("stm_id") or "").strip()

    if not stm_id:
        return jsonify({"error": "Missing 'stm_id'"}), 400

    try:
        entry = MEMORY.promote_stm_to_ltm(stm_id)
        if entry is None:
            return jsonify({"status": "not_found", "message": "No STM entry with that id"}), 404
        return jsonify({"status": "success", "entry": entry})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/memory/forget", methods=["POST"])
def memory_forget():
    global MEMORY

    if MEMORY is None:
        return jsonify({"error": "Memory system not initialized"}), 500

    data = request.get_json(silent=True) or {}
    tier = (data.get("tier") or "").lower().strip()
    mem_id = (data.get("id") or "").strip()

    if tier not in ("wm", "stm", "ltm"):
        return jsonify({"error": "Invalid or missing 'tier'. Use wm, stm, or ltm."}), 400
    if not mem_id:
        return jsonify({"error": "Missing 'id'"}), 400

    try:
        removed = MEMORY.forget_memory(tier=tier, mem_id=mem_id)
        return jsonify({"status": "success", "removed": removed})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/memory/reset", methods=["POST"])
def memory_reset():
    global MEMORY

    if MEMORY is None:
        return jsonify({"error": "Memory system not initialized"}), 500

    data = request.get_json(silent=True) or {}
    tier = (data.get("tier") or "").lower().strip()
    confirm = bool(data.get("confirm", False))

    if tier not in ("wm", "stm", "ltm", "all"):
        return jsonify({"error": "Invalid or missing 'tier'. Use wm, stm, ltm, or all."}), 400

    if not confirm:
        return jsonify({"error": "Reset requires 'confirm': true"}), 400

    try:
        MEMORY.reset_memory(tier=tier)
        return jsonify({"status": "success", "tier": tier})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/memory/search", methods=["POST"])
def memory_search():
    global MEMORY

    if MEMORY is None:
        return jsonify({"error": "Memory system not initialized"}), 500

    data = request.get_json(silent=True) or {}
    query = (data.get("query") or "").strip()
    tiers = data.get("tiers")

    if not query:
        return jsonify({"error": "Missing 'query'"}), 400

    if tiers is not None and isinstance(tiers, list):
        tiers = [str(t).lower().strip() for t in tiers if t]
    else:
        tiers = None

    try:
        results = MEMORY.search_memory(query=query, tiers=tiers)
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------
# MAIN
# -----------------------------------------------------
def main():
    global CONFIG, SYSTEM_PROMPT, MEMORY

    parser = argparse.ArgumentParser(description="Config-driven AI agent server")
    parser.add_argument("--config", required=True, help="Path to config JSON")
    parser.add_argument("--port", type=int, default=5001, help="Port to run on")
    args = parser.parse_args()

    # Load config & system prompt
    CONFIG = load_config(args.config)
    SYSTEM_PROMPT = load_system_prompt(CONFIG["system_prompt_path"])

    # Memory manager setup (per-agent)
    memory_dir = CONFIG["memory_dir"]
    if not os.path.isabs(memory_dir):
        memory_dir = os.path.join(ROOT_DIR, memory_dir)

    os.makedirs(memory_dir, exist_ok=True)
    MEMORY = MemoryManager(memory_dir=memory_dir)

    print("========================================")
    print("  Config-Driven Agent Server Starting")
    print("  Agent: ", CONFIG["agent_name"])
    print("  Model: ", CONFIG["model"])
    print("  Behavior Mode:", CONFIG.get("personality_mode"))
    print("  Memory Dir: ", memory_dir)
    print("  Port:", args.port)
    print("========================================")

    app.run(host="0.0.0.0", port=args.port, debug=False)


if __name__ == "__main__":
    main()
