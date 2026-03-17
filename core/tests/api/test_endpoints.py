"""
🧠 MEMORY ENDPOINT VALIDATOR
Quick test of all memory endpoints
"""

import requests
import json

def test_memory_endpoints():
    """Test all memory endpoints"""
    base_url = "http://127.0.0.1:5001"
    
    print("🧠 TESTING MEMORY ENDPOINTS")
    print("=" * 40)
    
    # Test 1: Health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health failed: {e}")
    
    # Test 2: Chat endpoint (basic)
    try:
        response = requests.post(
            f"{base_url}/chat", 
            json={"message": "Hello Nyra!"},
            timeout=10
        )
        print(f"✅ Chat: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ Chat failed: {e}")
    
    # Test 3: Memory stats
    try:
        response = requests.get(f"{base_url}/memory/stats", timeout=5)
        print(f"✅ Memory Stats: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Memory stats failed: {e}")
    
    # Test 4: Memory search
    try:
        response = requests.post(
            f"{base_url}/memory/search", 
            json={"query": "hello", "limit": 5},
            timeout=5
        )
        print(f"✅ Memory Search: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Memory search failed: {e}")
    
    print("\n🎉 ENDPOINT TESTING COMPLETE!")

if __name__ == "__main__":
    test_memory_endpoints()