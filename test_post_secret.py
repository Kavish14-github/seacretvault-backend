import requests

url = "http://127.0.0.1:8000/api/secrets/"
headers = {
    "Authorization": "Token ad0a5aa406daace918a789a987872cc00141b397",
    "Content-Type": "application/json"
}
payload = {
    "key": "kavish",
    "value": "supersecurepassword",
    "environment": 1
}

response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())
