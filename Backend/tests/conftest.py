import requests
import pytest

@pytest.fixture(scope="session")
def login_as_admin():
    payload = {"username":"Kevin", "password":"test"}
    response = requests.post("http://127.0.0.1:5000/login", json=payload)
    assert response.ok

    access_token = response.json()["access_token"]
    yield access_token