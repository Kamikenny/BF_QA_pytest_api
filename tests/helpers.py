import json
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_json(relative_path):
    with open(PROJECT_ROOT / relative_path, encoding="utf-8") as f:
        return json.load(f)


def login(base_url: str, email: str, password: str):
    payload = {
        "username": email,
        "password": password,
    }
    response = requests.post(
        f"{base_url}/api/auth/token",
        data=payload,
    )

    if response.status_code == 200:
        return response.json()
    return response.text


print(login("http://localhost:8000", "client@eventflow.test", "client1234"))
