import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file if present
load_dotenv()

# Read API key from environment variable for safety.
# Set GENAI_API_KEY in your environment instead of hard-coding secrets.
api_key = os.getenv("GENAI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    raise RuntimeError(
        "GENAI_API_KEY is not set. Set this environment variable or configure application default credentials."
    )

model = genai.GenerativeModel('gemini-2.5-pro')
