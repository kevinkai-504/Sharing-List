import requests
import pytest
from lib.utils import build_request_headers

def test_login(login_as_admin):
    request_header = build_request_headers(login_as_admin)
    response = requests.get("http://127.0.0.1:5000/learn",headers=request_header)
    assert response.ok