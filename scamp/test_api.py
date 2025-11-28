import requests

url = "http://127.0.0.1:8000/analyze"

files = {
    "file": open("test.jpg", "rb")  # make sure this path exists
}
data = {
    "media_type": "image",          # or "audio" later
    "user_id": "demo-user-1",
    "platform": "telegram"
}

resp = requests.post(url, files=files, data=data)
print("Status:", resp.status_code)
print("JSON:", resp.json())
