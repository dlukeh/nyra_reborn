import requests

url = "http://localhost:5001/api/chat"
payload = {"message": "Hello Nyra!", "session_id": "test-session"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error during POST request:", e)