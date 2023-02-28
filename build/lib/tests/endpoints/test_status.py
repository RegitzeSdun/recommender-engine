import os
import sys
import time

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.getcwd())

from recommender_engine.main import app

URL = "/v" + os.environ["API_VERSION"] + "/status"


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_01_get_status(client):
    response = client.get(URL, json={})

    assert response.status_code == 200
    #assert response.json() == {"status": "OK", "models": [{"2": 3}, {"1": 1}]}
