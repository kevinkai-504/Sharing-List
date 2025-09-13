import pytest
from config import APP_URL, LOG
from lib.user import User
import os

@pytest.fixture(scope="session")
def login_as_admin_token():
    LOG.info("login_as_admin_token")
    ADMIN_ACCOUNT = str(os.getenv("ADMIN_ACCOUNT"))
    ADMIN_PASSWORD = str(os.getenv("ADMIN_PASSWORD"))
    response = User().login(APP_URL, ADMIN_ACCOUNT, ADMIN_PASSWORD)
    assert response.ok

    access_token = response.json()["access_token"]
    yield access_token