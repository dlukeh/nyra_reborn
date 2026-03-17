
"""
auth_setup.py
------------------------------------
Gemini Pro 2 CLI authentication using API key.
No OAuth, no Flask routes, no redirect URIs.

Setup:
1. Add your Gemini API Key to .env as:
   GENAI_API_KEY=your_api_key_here
2. Run:
   python auth_setup.py
3. You should see Gemini respond in the terminal.

# TODO: Nyra initialization code will be added below this handshake once CLI test succeeds.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Retrieve API key
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("❌ Missing GENAI_API_KEY in .env — please add your Gemini API Key.")

# Configure Gemini client
genai.configure(api_key=api_key)

# Initialize model (Gemini 2.5 Pro)
# TODO (Copilot): auto-detect the highest available "gemini-x.x-pro" model via list_models()
model = genai.GenerativeModel("models/gemini-2.5-pro")

# Simple test prompt
prompt = "Hello Gemini Pro 2 — Nyra Systems CLI handshake test."

print("🤖 Sending request to Gemini Pro 2...")
reply = model.generate_content(prompt)

# Display response safely
print("\n✅ Gemini Response:\n")
if hasattr(reply, "text") and reply.text:
    print(reply.text)
else:
    print("(No text returned or unexpected response format.)")

print("\n🌐 CLI handshake complete — ready for Nyra integration.")


