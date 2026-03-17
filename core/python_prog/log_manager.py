import os
import json
from flask import Blueprint, jsonify, request

log_manager = Blueprint('log_manager', __name__)
REFLECTION_DIR = os.path.join(os.path.dirname(__file__), 'memory', 'logs', 'daily_reflections')

def load_logs():
    logs = []
    if not os.path.exists(REFLECTION_DIR):
        return logs
    for fname in os.listdir(REFLECTION_DIR):
        if fname.endswith('.json'):
            fpath = os.path.join(REFLECTION_DIR, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    entry = json.load(f)
                    logs.append(entry)
            except Exception:
                continue
    return logs

@log_manager.route('/api/logs', methods=['GET'])
def api_logs():
    q = request.args.get('q', '').lower()
    tags = request.args.get('tags', '').lower().split(',') if request.args.get('tags') else []
    logs = load_logs()
    filtered = []
    for log in logs:
        if q and q not in json.dumps(log).lower():
            continue
        if tags and not any(tag.strip() in (log.get('tags') or []) for tag in tags if tag.strip()):
            continue
        filtered.append(log)
    return jsonify({'logs': filtered})

@log_manager.route('/api/logs/stats', methods=['GET'])
def api_logs_stats():
    logs = load_logs()
    tones = {}
    tags = {}
    for log in logs:
        tone = log.get('emotional_tone', '—')
        tones[tone] = tones.get(tone, 0) + 1
        for tag in log.get('tags', []):
            tags[tag] = tags.get(tag, 0) + 1
    return jsonify({
        'total_logs': len(logs),
        'emotional_tones': tones,
        'tags': tags
    })
