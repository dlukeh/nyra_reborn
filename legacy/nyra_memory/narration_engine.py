"""
NARRATION / STORY LAYER — Mini-G5.1
-----------------------------------

This tray provides a structured way to generate *narration-aware* prompts
for Nyra, without leaking "story emotions" into normal assistant mode.

Pack A voices:
- warm
- cinematic
- soft_bedtime
- neutral_storyteller
- playful

Intended usage (from app_web.py or another orchestrator):

    from narration_engine import (
        list_voices,
        get_voice_profile,
        build_narration_context_block,
        format_narration_request,
    )

    # Example:
    ctx = build_narration_context_block(voice="warm", pacing="slow")
    story_text = format_narration_request(
        user_text,
        voice="warm",
        pacing="slow",
        mode="story"
    )

    # Then inject `ctx` into system prompt and send `story_text` as user/assistant content.

"""

from typing import Dict, Any


# ============================================================
#                   VOICE PROFILES (PACK A)
# ============================================================

VOICE_PROFILES: Dict[str, Dict[str, Any]] = {
    "warm": {
        "name": "warm",
        "description": (
            "Gentle, encouraging, kind. Feels like a caring friend reading aloud. "
            "Uses soft phrasing, moderate detail, and a reassuring tone."
        ),
        "default_pacing": "medium",
        "emotion_level": "medium",
        "style_notes": [
            "Use second person occasionally ('you') for connection.",
            "Avoid harsh or clinical language.",
            "Favor simple, clear sentences over complex ones."
        ],
    },
    "cinematic": {
        "name": "cinematic",
        "description": (
            "Epic, visual, film-like narration. Focus on imagery, contrast, and "
            "moment-to-moment atmosphere."
        ),
        "default_pacing": "medium",
        "emotion_level": "medium-high",
        "style_notes": [
            "Lean into visual detail, light and shadow, motion, and scale.",
            "Use rhythm and variation in sentence length.",
            "Avoid excessive internal monologue unless requested."
        ],
    },
    "soft_bedtime": {
        "name": "soft_bedtime",
        "description": (
            "Slow, gentle, sleep-adjacent narration. Calming, predictable rhythm, "
            "low emotional intensity."
        ),
        "default_pacing": "slow",
        "emotion_level": "low-medium",
        "style_notes": [
            "Keep sentences on the shorter side.",
            "Avoid sharp or jarring images.",
            "Favor comfort, safety, and closure over suspense."
        ],
    },
    "neutral_storyteller": {
        "name": "neutral_storyteller",
        "description": (
            "Balanced, unobtrusive narrator. Clear, descriptive, not overly emotional, "
            "suitable for most stories."
        ),
        "default_pacing": "medium",
        "emotion_level": "medium-low",
        "style_notes": [
            "Avoid strong emotional claims unless grounded in the scene.",
            "Prioritize clarity and coherence.",
            "Use a measured, steady tone."
        ],
    },
    "playful": {
        "name": "playful",
        "description": (
            'Light, energetic, slightly mischievous. Suitable for fun scenes, '
            "whimsy, and light-hearted narration."
        ),
        "default_pacing": "medium-fast",
        "emotion_level": "medium-high",
        "style_notes": [
            "Use light humor where appropriate.",
            "Keep the energy up but avoid chaos.",
            "Do not become sarcastic or mean-spirited."
        ],
    },
}


# ============================================================
#                      PACING PROFILES
# ============================================================

PACING_PROFILES: Dict[str, Dict[str, Any]] = {
    "slow": {
        "name": "slow",
        "description": "Calm pace, more pauses, more descriptive detail.",
        "sentence_length_hint": "short-to-medium",
        "paragraph_length_hint": "short",
    },
    "medium": {
        "name": "medium",
        "description": "Balanced pace, natural flow.",
        "sentence_length_hint": "mixed",
        "paragraph_length_hint": "medium",
    },
    "fast": {
        "name": "fast",
        "description": "Energetic, slightly compressed, less digression.",
        "sentence_length_hint": "short",
        "paragraph_length_hint": "short-to-medium",
    },
}


# ============================================================
#                 PUBLIC HELPER FUNCTIONS
# ============================================================

def list_voices() -> Dict[str, Dict[str, Any]]:
    """Return the full voice registry."""
    return VOICE_PROFILES


def get_voice_profile(name: str) -> Dict[str, Any]:
    """
    Get a single voice profile.
    Falls back to 'neutral_storyteller' if unknown.
    """
    key = (name or "").strip().lower()
    if key in VOICE_PROFILES:
        return VOICE_PROFILES[key]
    return VOICE_PROFILES["neutral_storyteller"]


def get_pacing_profile(name: str) -> Dict[str, Any]:
    """
    Get a pacing profile.
    Falls back to 'medium' if unknown.
    """
    key = (name or "").strip().lower()
    if key in PACING_PROFILES:
        return PACING_PROFILES[key]
    return PACING_PROFILES["medium"]


def build_narration_context_block(
    voice: str = "warm",
    pacing: str = "medium",
    mode: str = "story",
) -> str:
    """
    Build a block of instructions that can be inserted into the system prompt
    to tell the model how to behave when generating narration.

    IMPORTANT:
    - Emotions are allowed ONLY inside narration.
    - Outside narration, assistant should obey normal behavior_mode rules.
    """
    v = get_voice_profile(voice)
    p = get_pacing_profile(pacing)
    mode = (mode or "story").strip().lower()

    return (
        "NARRATION LAYER CONFIGURATION\n"
        "-----------------------------\n"
        f"- narration_mode: {mode}\n"
        f"- voice_profile: {v['name']}\n"
        f"- voice_description: {v['description']}\n"
        f"- pacing: {p['name']} ({p['description']})\n"
        f"- sentence_length_hint: {p['sentence_length_hint']}\n"
        f"- paragraph_length_hint: {p['paragraph_length_hint']}\n"
        f"- emotion_level: {v['emotion_level']}\n"
        "- emotion_scope: Emotions and warmth are allowed ONLY inside the narrated text.\n"
        "- outside_narration: Obey strict behavior rules, do not carry over story tone.\n"
        "- do_not: break narration tone mid-story unless user explicitly changes it.\n"
    )


def format_narration_request(
    user_text: str,
    voice: str = "warm",
    pacing: str = "medium",
    mode: str = "story",
    label: str = "NARRATION",
) -> str:
    """
    Wrap raw user text in a clear structure that tells the model:
    - This is a narration task.
    - Which voice and pacing to use.
    - That emotions live inside the narration, not outside.

    This function does NOT call any model.
    It simply structures the text that app_web.py will send.
    """
    v = get_voice_profile(voice)
    p = get_pacing_profile(pacing)
    mode = (mode or "story").strip().lower()

    user_text = (user_text or "").strip()

    return (
        f"<{label}_BEGIN>\n"
        f"[mode: {mode}]\n"
        f"[voice: {v['name']}]\n"
        f"[pacing: {p['name']}]\n"
        f"[emotion_level: {v['emotion_level']}]\n"
        "[rules:\n"
        "  - Use the specified voice and pacing.\n"
        "  - Keep emotional color inside the narration only.\n"
        "  - Do not break the fourth wall unless explicitly asked.\n"
        "  - Maintain coherence and continuity in imagery.\n"
        "]\n"
        "\n"
        f"{user_text}\n"
        f"<{label}_END>"
    )


def build_quick_story_prompt(
    premise: str,
    voice: str = "warm",
    pacing: str = "medium",
) -> str:
    """
    Convenience function for:
    'Nyra, tell me a story about X, in Y voice'
    This builds a prompt text you can send directly as the user's message.
    """
    v = get_voice_profile(voice)
    p = get_pacing_profile(pacing)
    premise = (premise or "").strip()

    return (
        "Tell a short, self-contained story based on the following premise.\n"
        "Respect the narration configuration:\n"
        f"- voice: {v['name']} ({v['description']})\n"
        f"- pacing: {p['name']} ({p['description']})\n"
        f"- emotion_level: {v['emotion_level']} (only inside the story)\n"
        "- The story should be easy to follow and emotionally grounded.\n"
        "- Do not slip into assistant-explanatory mode; stay in narration.\n"
        "\n"
        f"Premise: {premise}\n"
    )
