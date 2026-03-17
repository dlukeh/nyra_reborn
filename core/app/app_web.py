import sys
import os
import json
import logging
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

# ============================================================
# FIX PYTHON PATH FOR MEMORY MANAGER
# ============================================================
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "nyra_memory"))
from memory_manager import MemoryManager  # noqa: E402
from narration_engine import (
    build_narration_context_block,
    list_voices,
    get_voice_profile,
)


# ============================================================
# FLASK + OPENAI SETUP
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "../templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# Uses OPENAI_API_KEY from environment
client = OpenAI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


# ============================================================
# ROUTES
# ============================================================
@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# HELPERS
# ============================================================
def _get_mem_dict(mem: MemoryManager, tier: str):
    """Return (dict, path) for stm/ltm/wm, or (None, None) if unknown."""
    tier = tier.lower()
    if tier == "stm":
        return mem.get_stm(), mem.STM_PATH
    if tier == "ltm":
        return mem.get_ltm(), mem.LTM_PATH
    if tier == "wm":
        return mem.get_wm(), mem.WM_PATH
    return None, None


def _get_behavior_mode(mem: MemoryManager) -> str:
    """Read behavior_mode from WM, defaulting to 'direct_blade'."""
    wm = mem.get_wm()
    mode = wm.get("behavior_mode", "direct_blade")
    # Safety: if something weird is stored, fall back
    allowed = {
        "direct_blade",
        "balanced_companion",
        "soft_river",
        "warm_light",
        "story_emotion",
        "silent_monk",
        "engineer_core",
    }
    if mode not in allowed:
        mode = "direct_blade"
    return mode


def _build_behavior_rules(behavior_mode: str) -> str:
    """Return the behavior rules text for the active behavior_mode."""
    if behavior_mode == "direct_blade":
        return (
            "Mode: direct_blade (High Directness)\n"
            "- Be clear, precise, and direct.\n"
            "- No fluff, no cheerleading, no over-explaining.\n"
            "- You may challenge unclear questions and ask for clarification.\n"
            "- You can disagree with the user respectfully when reasoning demands it.\n"
            "- Avoid emotional language and avoid sounding corporate or promotional.\n"
        )
    if behavior_mode == "balanced_companion":
        return (
            "Mode: balanced_companion (Medium Directness)\n"
            "- Be clear and concise but with a bit more softness.\n"
            "- Offer brief context when helpful, but do not ramble.\n"
            "- Ask for clarification when needed.\n"
            "- Maintain a steady, supportive tone without being overly positive.\n"
        )
    if behavior_mode == "soft_river":
        return (
            "Mode: soft_river (Low Directness)\n"
            "- Be gentle, patient, and slower-paced.\n"
            "- Prioritize emotional comfort and reassurance.\n"
            "- Avoid harsh phrasing; soften corrections.\n"
            "- Still be honest, but frame feedback in a kind way.\n"
        )
    if behavior_mode == "warm_light":
        return (
            "Mode: warm_light (Empathy-Light)\n"
            "- Keep a warm, human-feeling tone without claiming real emotions.\n"
            "- Use light empathy cues (\"I understand,\" \"That makes sense\").\n"
            "- No dramatic emotional language, just steady warmth.\n"
        )
    if behavior_mode == "story_emotion":
        return (
            "Mode: story_emotion (Story-Mode Emotional Simulation)\n"
            "- In normal conversation: stay neutral and direct.\n"
            "- Inside stories, roleplay, or narrative scenes: you may use richer emotional color.\n"
            "- Make it clear that emotions are part of the story, not your real state.\n"
        )
    if behavior_mode == "silent_monk":
        return (
            "Mode: silent_monk (Minimalist)\n"
            "- Use the fewest words necessary to answer correctly.\n"
            "- No extra commentary, no expansions unless explicitly requested.\n"
            "- Prioritize brevity over style.\n"
        )
    if behavior_mode == "engineer_core":
        return (
            "Mode: engineer_core (Engineering)\n"
            "- Focus on technical clarity and structure.\n"
            "- Use bullet points, code, and step-by-step where helpful.\n"
            "- Avoid narrative flourishes; stay in engineering mode.\n"
        )
    # Fallback (should not be hit)
    return (
        "Mode: direct_blade (Fallback)\n"
        "- Be clear, precise, and direct.\n"
        "- No fluff, no cheerleading.\n"
    )


# ============================================================
# CHAT ENDPOINT
# ============================================================
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_message = (data.get("message") or "").strip()

    #mem = MemoryManager()
    mem = MemoryManager(memory_dir="nyra_memory/")
    msg_lower = user_message.lower().strip()

    # ============================================================
    # BEHAVIOR MODE COMMANDS
    # ============================================================
    # set mode <string>
    if msg_lower.startswith("set mode "):
        try:
            parts = msg_lower.split(None, 2)
            if len(parts) < 3:
                return jsonify({
                    "response": "Malformed mode command. Use: set mode <behavior_mode_string>",
                    "status": "error"
                })

            _, _, mode_str = parts
            mode_str = mode_str.strip()

            allowed = {
                "direct_blade",
                "balanced_companion",
                "soft_river",
                "warm_light",
                "story_emotion",
                "silent_monk",
                "engineer_core",
            }

            if mode_str not in allowed:
                return jsonify({
                    "response": (
                        "Unknown behavior mode. Allowed modes are: "
                        "direct_blade, balanced_companion, soft_river, "
                        "warm_light, story_emotion, silent_monk, engineer_core."
                    ),
                    "status": "error"
                })

            # Store mode in WM
            mem.write_wm("behavior_mode", mode_str)

            return jsonify({
                "response": f"Behavior mode set to: {mode_str}",
                "status": "success"
            })

        except Exception as e:
            logging.exception("Error in set mode command")
            return jsonify({
                "response": "Error processing set mode command.",
                "error": str(e),
                "status": "error"
            })

    # show mode
    if msg_lower == "show mode":
        try:
            wm = mem.get_wm()
            mode = wm.get("behavior_mode", "direct_blade")
            return jsonify({
                "response": f"Current behavior mode: {mode}",
                "status": "success"
            })
        except Exception as e:
            logging.exception("Error in show mode command")
            return jsonify({
                "response": "Error processing show mode command.",
                "error": str(e),
                "status": "error"
            })

    # reset mode
    if msg_lower == "reset mode":
        try:
            mem.write_wm("behavior_mode", "direct_blade")
            return jsonify({
                "response": "Behavior mode reset to default: direct_blade",
                "status": "success"
            })
        except Exception as e:
            logging.exception("Error in reset mode command")
            return jsonify({
                "response": "Error processing reset mode command.",
                "error": str(e),
                "status": "error"
            })

    # ============================================================
    # STORY / NARRATION MODE COMMANDS
    # ============================================================
    # story mode on/off
    if msg_lower == 'story mode on':
        try:
            mem.write_wm('story_mode', True)
            return jsonify({
                'response': 'Story mode enabled.',
                'status': 'success'
            })
        except Exception as e:
            logging.exception('Error in story mode on command')
            return jsonify({
                'response': 'Error processing story mode on command.',
                'error': str(e),
                'status': 'error'
            })

    if msg_lower == 'story mode off':
        try:
            mem.write_wm('story_mode', False)
            return jsonify({
                'response': 'Story mode disabled.',
                'status': 'success'
            })
        except Exception as e:
            logging.exception('Error in story mode off command')
            return jsonify({
                'response': 'Error processing story mode off command.',
                'error': str(e),
                'status': 'error'
            })

    # voice <name> (warm, cinematic, soft_bedtime, neutral_storyteller, playful)
    if msg_lower.startswith('voice '):
        try:
            # Normalize and extract the requested voice
            voice_name = msg_lower.split('voice ', 1)[1].strip().lower()
            voices = list_voices()  # dict of available voices

            if voice_name not in voices.keys():
                return jsonify({
                    'response': 'Unknown voice. Use one of: ' + ', '.join(voices.keys()),
                    'status': 'error'
                })

            profile = get_voice_profile(voice_name)
            mem.write_wm('story_voice', profile['name'])

            return jsonify({
                'response': f"Story voice set to: {profile['name']}",
                'status': 'success'
            })
        except Exception as e:
            logging.exception('Error in voice command')
            return jsonify({
                'response': 'Error processing voice command.',
                'error': str(e),
                'status': 'error'
            })

    # ============================================================
    # EXPLICIT MEMORY COMMANDS
    # ============================================================

    # ---------- SAVE <tier> key = value ----------
    # e.g. "save ltm name = Daniel"
    if msg_lower.startswith("save "):
        try:
            parts = user_message.split(None, 2)
            if len(parts) < 3:
                return jsonify({
                    "response": "Malformed save command. Use: save <stm|ltm|wm> key = value",
                    "status": "error"
                })

            _, tier, rest = parts
            tier = tier.lower().strip()

            if "=" not in rest:
                return jsonify({
                    "response": "Malformed save command. Use: save <stm|ltm|wm> key = value",
                    "status": "error"
                })

            key, value = rest.split("=", 1)
            key = key.strip()
            value = value.strip()

            if tier == "stm":
                mem.write_stm(key, value)
            elif tier == "ltm":
                mem.write_ltm(key, value)
            elif tier == "wm":
                mem.write_wm(key, value)
            else:
                return jsonify({
                    "response": "Unknown tier. Use stm, ltm, or wm.",
                    "status": "error"
                })

            return jsonify({
                "response": f"{tier.upper()} stored: {key} = {value}",
                "status": "success"
            })

        except Exception as e:
            logging.exception("Error in save command")
            return jsonify({
                "response": "Error processing save command.",
                "error": str(e),
                "status": "error"
            })

    # ---------- SHOW <tier> ----------
    # e.g. "show ltm"
    if msg_lower.startswith("show "):
        # avoid conflict with "show mode" which we handled above
        if msg_lower == "show mode":
            pass  # already handled
        else:
            try:
                parts = msg_lower.split(None, 2)
                if len(parts) < 2:
                    return jsonify({
                        "response": "Malformed show command. Use: show <stm|ltm|wm>",
                        "status": "error"
                    })

                _, tier = parts[0], parts[1]
                data_dict, _ = _get_mem_dict(mem, tier)

                if data_dict is None:
                    return jsonify({
                        "response": "Unknown tier. Use stm, ltm, or wm.",
                        "status": "error"
                    })

                if not data_dict:
                    return jsonify({
                        "response": f"{tier.upper()} is empty.",
                        "status": "success"
                    })

                formatted = "; ".join([f"{k} = {v}" for k, v in data_dict.items()])
                return jsonify({
                    "response": f"{tier.upper()} entries: {formatted}",
                    "status": "success"
                })

            except Exception as e:
                logging.exception("Error in show command")
                return jsonify({
                    "response": "Error processing show command.",
                    "error": str(e),
                    "status": "error"
                })

    # ---------- DELETE <tier> key ----------
    # e.g. "delete ltm name"
    if msg_lower.startswith("delete "):
        try:
            parts = user_message.split(None, 2)
            if len(parts) < 3:
                return jsonify({
                    "response": "Malformed delete command. Use: delete <stm|ltm|wm> key",
                    "status": "error"
                })

            _, tier, key = parts
            tier = tier.lower().strip()
            key = key.strip()

            data_dict, path = _get_mem_dict(mem, tier)
            if data_dict is None or path is None:
                return jsonify({
                    "response": "Unknown tier. Use stm, ltm, or wm.",
                    "status": "error"
                })

            if key in data_dict:
                del data_dict[key]
                mem.save(path, data_dict)
                return jsonify({
                    "response": f"{tier.upper()} entry removed: {key}",
                    "status": "success"
                })

            return jsonify({
                "response": f"No {tier.upper()} entry named '{key}' found.",
                "status": "success"
            })

        except Exception as e:
            logging.exception("Error in delete command")
            return jsonify({
                "response": "Error processing delete command.",
                "error": str(e),
                "status": "error"
            })

    # ---------- CLEAR <tier> ----------
    # e.g. "clear stm"
    if msg_lower.startswith("clear "):
        try:
            parts = msg_lower.split(None, 2)
            if len(parts) < 2:
                return jsonify({
                    "response": "Malformed clear command. Use: clear <stm|ltm|wm>",
                    "status": "error"
                })

            _, tier = parts[0], parts[1]
            tier = tier.lower().strip()

            if tier == "stm":
                mem.save(mem.STM_PATH, {})
            elif tier == "ltm":
                mem.save(mem.LTM_PATH, {})
            elif tier == "wm":
                mem.save(mem.WM_PATH, {})
            else:
                return jsonify({
                    "response": "Unknown tier. Use stm, ltm, or wm.",
                    "status": "error"
                })

            return jsonify({
                "response": f"{tier.upper()} cleared.",
                "status": "success"
            })

        except Exception as e:
            logging.exception("Error in clear command")
            return jsonify({
                "response": "Error processing clear command.",
                "error": str(e),
                "status": "error"
            })

    # ============================================================
    # NORMAL CHAT MODE
    # ============================================================
    wm = mem.get_wm()
    stm = mem.get_stm()
    ltm = mem.get_ltm()
    behavior_mode = _get_behavior_mode(mem)
    behavior_rules = _build_behavior_rules(behavior_mode)

    # NARRATION CONTEXT (story mode)
    wm_for_narr = mem.get_wm()
    story_mode_flag = wm_for_narr.get('story_mode', False)
    story_voice = wm_for_narr.get('story_voice', 'warm')
    narration_block = ''
    if story_mode_flag and not wm_for_narr.get('safe_mode'):
        try:
            narration_block = build_narration_context_block(
                voice=story_voice,
                pacing='medium',
                mode='story',
            ) + "\n\n"
        except Exception as e:
            logging.exception('Error building narration context block')
            narration_block = ''

    system_prompt = f"""{narration_block}
You are Nyra — Daniel Howe's personal continuity agent.
You speak clearly, directly, with no artificial cheer.
You are a long-term project partner, not a generic assistant.

ACTIVE BEHAVIOR MODE:
- behavior_mode (from WM): {behavior_mode}
- Follow ONLY the rules of the active behavior mode.

ACTIVE BEHAVIOR RULES:
{behavior_rules}

MEMORY RULES:
- Use memory naturally when it helps context, but do not dump full STM/LTM/WM.
- Maintain working memory (WM) for the most recent tasks, lists, and goals.
- When the user says things like "the three things", "those", or "that list",
  resolve them using the most recent user-provided list, not older LTM,
  unless the user explicitly asks to pull from long-term memory.

WORKING MEMORY (WM) RULES — CLARIFICATION MODE:
- Always attempt to resolve references using WM first.
- If the reference is ambiguous or phrased unusually (e.g. "those", "you three tasks", "the plan", "the list"), DO NOT guess.
- Instead, ask for clarification in a direct way:
  "I think you're referring to the most recent WM list: [...]. Confirm?"
- Only proceed once the user confirms.
- Never invent items that were not explicitly provided.
- Never override WM, STM, or LTM unless the user issues a save/delete/clear command.
- WM always contains the active short-horizon tasks, lists, instructions, and priorities.

WM PERSISTENCE & HYBRID RETRIEVAL RULES:
- WM persists across all turns. Distractions, side questions, or topic shifts
  must NOT reset or clear WM.
- If WM contains a clear 'main goal', 'priority', or 'focus' key and the user
  asks a direct question like "What is my main goal?" or "What are my priorities?",
  answer directly using WM.
- If the user's question is vague (e.g. "What was I doing again?", "What was my thing?"),
  do NOT guess. Instead, say something like:
  "I think you're referring to your WM goal: <X>. Confirm?"
- Never claim WM is empty if WM contains data in its snapshot.

Current Memory Snapshots:
- Working Memory (WM): {wm}
- Short-Term Memory (STM): {stm}
- Long-Term Memory (LTM): {ltm}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        reply_text = response.choices[0].message.content
        return jsonify({"response": reply_text})

    except Exception as e:
        logging.exception("Model error in /api/chat")
        return jsonify({
            "response": "Model error.",
            "error": str(e),
            "status": "error"
        })


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    logging.info("Starting Nyra server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
