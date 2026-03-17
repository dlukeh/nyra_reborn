import requests

url = "http://localhost:5001/api/command"
payload = {"command": "test"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers, timeout=5)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error during POST request:", e)
