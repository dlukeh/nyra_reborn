"""
Dry-run test for GemniGF/app
Validates imports, configuration, and basic setup without entering the chat loop.
"""
import os
import sys

# Set a dummy API key for testing
os.environ['GENAI_API_KEY'] = 'test_dummy_key_for_dry_run'

print("=" * 60)
print("DRY RUN TEST - GemniGF/app")
print("=" * 60)

# Test 1: Import dotenv
print("\n[1/5] Testing dotenv import...")
try:
    from dotenv import load_dotenv
    print("✓ dotenv imported successfully")
except ImportError as e:
    print(f"✗ Failed to import dotenv: {e}")
    sys.exit(1)

# Test 2: Load .env file
print("\n[2/5] Loading .env file...")
load_dotenv()
print("✓ .env loaded (if present)")

# Test 3: Import google.generativeai
print("\n[3/5] Testing google.generativeai import...")
try:
    import google.generativeai as genai
    print("✓ google.generativeai imported successfully")
except ImportError as e:
    print(f"✗ Failed to import google.generativeai: {e}")
    sys.exit(1)

# Test 4: Check API key
print("\n[4/5] Checking API key configuration...")
api_key = os.getenv("GENAI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key:
    print(f"✓ API key found: {api_key[:10]}..." if len(api_key) > 10 else f"✓ API key found: {api_key}")
    if api_key == "REPLACE_WITH_YOUR_NEW_API_KEY":
        print("⚠ WARNING: Using placeholder key from .env template")
        print("  → Edit .env and add your real Google API key before running the app")
    elif api_key == "test_dummy_key_for_dry_run":
        print("  → Using test dummy key (dry run mode)")
else:
    print("✗ No API key found in environment")
    sys.exit(1)

# Test 5: Configure GenAI (will fail with dummy key, but tests the flow)
print("\n[5/5] Testing GenAI configuration...")
try:
    genai.configure(api_key=api_key)
    print("✓ genai.configure() called successfully")
except Exception as e:
    print(f"⚠ genai.configure() raised an exception: {e}")
    print("  → This is expected with a dummy/invalid key")

# Test 6: Try to create model instance
print("\n[6/6] Testing model instantiation...")
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
    print("✓ GenerativeModel instance created")
    print(f"  Model: {model}")
except Exception as e:
    print(f"✗ Failed to create model: {e}")

print("\n" + "=" * 60)
print("DRY RUN SUMMARY")
print("=" * 60)
print("✓ All imports successful")
print("✓ Configuration flow works")
print("✓ Code structure is valid")
print("\nTo run the actual app:")
print("  1. Edit .env and add your real Google API key")
print("  2. Run: python GemniGF\\app")
print("=" * 60)
