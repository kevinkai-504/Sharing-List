import pytest
from lib.learn import Learn
from config import APP_URL

def test_login(login_as_admin):
    response = Learn().get_all_learns(APP_URL, login_as_admin)
    assert response.ok