"""
🎮 ENHANCED CLIENT TEST - Quick test of client with enhanced server
Testing if the original client works with our memory-enhanced server
"""

import requests

def test_client_compatibility():
    """Test if we need to update the client for the enhanced server"""
    base_url = "http://127.0.0.1:5000"
    
    print("🎮 TESTING CLIENT COMPATIBILITY")
    print("=" * 40)
    
    # Test the original endpoint the client expects
    try:
        response = requests.post(
            f"{base_url}/api/command",
            json={"command": "Hello Nyra!"},
            timeout=5
        )
        print(f"✅ /api/command: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ /api/command failed: {e}")
    
    # Test the new chat endpoint  
    try:
        response = requests.post(
            f"{base_url}/chat",
            json={"message": "Hello Nyra!"},
            timeout=5
        )
        print(f"✅ /chat: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ /chat failed: {e}")
    
    # Test export endpoint
    try:
        response = requests.get(f"{base_url}/api/export", timeout=5)
        print(f"✅ /api/export: {response.status_code}")
    except Exception as e:
        print(f"❌ /api/export failed: {e}")
    
    print("\n🎉 COMPATIBILITY TEST COMPLETE!")

if __name__ == "__main__":
    test_client_compatibility()