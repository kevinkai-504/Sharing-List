import pytest
from lib.learn import Learn
from config import APP_URL, LOG

def test_get_all_learns(login_as_admin):
    LOG.info("get_all_learns()")
    response = Learn().get_all_learns(APP_URL, login_as_admin)
    LOG.debug(response.json())
    assert response.ok