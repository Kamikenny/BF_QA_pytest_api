import requests
from rich import print

BASE_URL = "http://localhost:8000"
TIMEOUT = 5


def test_health_is_ok():
    response = requests.get(f"{BASE_URL}/api/health", timeout=TIMEOUT)

    assert response.status_code == 200, response.text
    assert response.headers["content-type"].startswith("application/json"), (
        response.headers["content-type"]
    )
    assert response.json()["status"] == "ok"
