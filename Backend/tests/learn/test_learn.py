import requests
import pytest
from lib.utils import build_request_headers
from lib.learn import Learn

def test_login(login_as_admin):
    response = Learn().get_all_learns("http://127.0.0.1:5000", login_as_admin)
    assert response.ok