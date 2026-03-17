"""
Minimal Flask dashboard for agent status, memory, and logs.
"""
from flask import Flask, render_template, jsonify
import os
import json

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/memory')
def memory():
    ltm = {}
    stm = {}
    if os.path.exists('ltm.json'):
        with open('ltm.json', 'r') as f:
            ltm = json.load(f)
    if os.path.exists('stm.json'):
        with open('stm.json', 'r') as f:
            stm = json.load(f)
    return jsonify({'ltm': ltm, 'stm': stm})

if __name__ == '__main__':
    app.run(debug=True)
