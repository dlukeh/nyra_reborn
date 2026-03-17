"""
TODO (Copilot + Danny): Verify which Gemini models this API key can access.
Purpose:
  The API key handshake succeeded, but the 'gemini-1.5-pro' model
  returned a 404 (NotFound). We’ll enumerate all accessible models
  and switch to the first compatible one (likely 'gemini-1.5-flash').

Steps:
  1. Load .env → read GENAI_API_KEY.
  2. Configure the Gemini client.
  3. List all available models via genai.list_models().
  4. Print the model names for inspection.
  5. Once confirmed, update auth_setup.py with a valid model name.
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

print("📦 Checking available Gemini models...\n")

# List all accessible models
try:
    for m in genai.list_models():
        print("-", m.name)
except Exception as e:
    print(f"❌ Error listing models: {e}")

print("\n✅ Done. Choose the correct model (e.g., 'models/gemini-1.5-flash') "
      "and replace it in auth_setup.py under:")
print("    model = genai.GenerativeModel('models/gemini-1.5-flash')")
