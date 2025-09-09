import requests
import pytest

def test_login():
    payload = {"username":"Kevin", "password":"test"}
    response = requests.post("http://127.0.0.1:5000/login", json=payload)
    assert response.ok 