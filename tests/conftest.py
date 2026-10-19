import os

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    """URL de l'API. Lue dans API_URL pour pouvoir viser un autre environnement."""
    return os.getenv("API_URL", "http://localhost:8000")
