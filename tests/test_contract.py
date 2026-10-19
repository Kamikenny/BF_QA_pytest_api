import pytest
import requests
from helpers import TIMEOUT, load_json
from jsonschema import ValidationError, validate

EVENT_SCHEMA = load_json("schemas/event.schema.json")

CATALOGUE_SCHEMA = {
    "type": "array",
    "minItems": 1,
    "items": EVENT_SCHEMA,
}


def test_contrat_event_valide(base_url):
    response = requests.get(f"{base_url}/api/events", timeout=TIMEOUT).json()

    validate(response, CATALOGUE_SCHEMA)


def test_schema_peut_echouer(base_url):
    response = requests.get(f"{base_url}/api/events", timeout=TIMEOUT).json()
    event = response[0]
    schema = load_json("schemas/event.schema.json")
    del event["id"]
    with pytest.raises(ValidationError):
        validate(event, schema)
