import requests
import pytest

EVENTS_URL = "http://localhost:8000/api/events"
TIMEOUT = 5


def test_events_structure_is_ok():

    response = requests.get(EVENTS_URL, timeout=TIMEOUT)
    events_lst = response.json()

    # Check statut et type de contenu conforme
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert type(events_lst) == list

    # Check structure schéma
    for event in events_lst:
        assert type(event["id"]) == int
        assert type(event["title"]) == str
        assert type(event["description"]) == str
        assert type(event["city"]) == str
        assert type(event["venue"]) == str
        assert type(event["starts_at"]) == str
        assert type(event["capacity"]) == int
        assert type(event["status"]) == str
        assert type(event["cover_color"]) == str


def test_events_published_only():

    response = requests.get(EVENTS_URL, timeout=TIMEOUT)
    events_lst = response.json()

    assert response.status_code == 200, response.json()["detail"]

    for event in events_lst:
        assert event["status"] == "published"


def test_events_response_not_empty():

    response = requests.get(EVENTS_URL, timeout=TIMEOUT)
    assert response.status_code == 200

    assert len(response.json()) > 0


@pytest.mark.parametrize(
    "event_id, expected_code",
    [
        (1, 200),
        (999999999, 404),
        ("", 200),
        ("abc", 422),
        (1.1, 422),
        (-1, 404),
    ],
    ids=[
        "Valide",
        "Introuvable",
        "String vide",
        "String abc",
        "Decimale",
        "Int negatif",
    ],
)
def test_event_id_requests(event_id, expected_code):

    response = requests.get(EVENTS_URL + f"/{event_id}", timeout=TIMEOUT)

    assert response.status_code == expected_code, response.text


@pytest.mark.parametrize(
    "test_params, expected_status, is_empty",
    [
        ({"q": ""}, 200, False),
        ({"q": "JAZZ"}, 200, False),
        ({"q": "jazz"}, 200, False),
        ({"q": "hufrmùuhù<ohf"}, 200, True),
        ({"q": False}, 200, True),
        ({}, 200, False),
    ],
    ids=[
        "String vide",
        "JAZZ",
        "jazz",
        "string introuvable",
        "integer",
        "params vide",
    ],
)
def test_events_requests_q(test_params, expected_status, is_empty):
    response = requests.get(EVENTS_URL, params=test_params, timeout=TIMEOUT)

    assert (
        response.status_code == expected_status
        and (len(response.json()) == 0) == is_empty
    )


@pytest.mark.parametrize(
    "transformation",
    [
        (lambda m: m),
        (str.upper),
        (str.lower),
    ],
    ids=[
        "Mot simple",
        "Mot majuscules",
        "Mot minuscules",
    ],
)
def test_events_q_trouve_event(transformation):
    response = requests.get(EVENTS_URL, timeout=TIMEOUT)
    assert response.status_code == 200, "La requête a échoué. Test impossible"

    events = response.json()
    assert len(events) > 0, "La liste d'événements est vide. Test impossible"

    mot = events[0]["title"].split()[0]

    test_params = {
        "q": transformation(mot),
    }

    sorted_events = requests.get(EVENTS_URL, params=test_params, timeout=TIMEOUT).json()

    assert events[0]["id"] in [e["id"] for e in sorted_events]


@pytest.mark.parametrize(
    "test_params, expected_status, expected_length",
    [
        ({"city": ""}, 200, 1),
        ({"city": "Bruxelles"}, 200, 1),
        ({"city": "bruxelles"}, 200, 0),
        ({"city": "Alpha"}, 200, 1),
        ({"city": ""}, 200, 1),
        ({"city": ""}, 200, 1),
    ],
)
def test_events_requests_city(test_params, expected_status, expected_length):
    pass
