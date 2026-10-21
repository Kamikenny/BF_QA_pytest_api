import pytest
import requests
from helpers import TIMEOUT, load_json
from jsonschema import ValidationError, validate

ORDER_RESPONSE_SCHEMA = load_json("schemas/order_response.schema.json")


def test_create_order(base_url, auth_headers):

    payload = {
        "event_id": 3,
        "items": [
            {
                "category_id": 8,
                "quantity": 6,
            }
        ],
        "promo_code": "",
    }
    response = requests.post(
        f"{base_url}/api/orders", json=payload, timeout=TIMEOUT, headers=auth_headers
    )
    assert response.status_code == 201
    validate(response.json(), ORDER_RESPONSE_SCHEMA)
