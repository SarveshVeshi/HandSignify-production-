import requests
import json

url = "https://handsignify.vercel.app/api/predict"
headers = {"Content-Type": "application/json"}
# Dummy landmarks data (21 points)
data = {"landmarks": [{"x": 0.1, "y": 0.1, "z": 0.1} for _ in range(21)]}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
except Exception as e:
    print(f"Request failed: {e}")
