import pytest
from config import SESSION, APP_URL, ADMIN_ACCOUNT, ADMIN_PASSWORD, LOG
@pytest.fixture(scope="session")
def login_as_admin():
    LOG.info("login_as_admin()")
    payload = {"username":ADMIN_ACCOUNT, "password":ADMIN_PASSWORD}
    LOG.info(f"Login in payload:{payload}")
    response = SESSION.post(f"{APP_URL}/login", json=payload)
    assert response.ok

    access_token = response.json()["access_token"]
    yield access_token