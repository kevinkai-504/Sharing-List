import pytest
from config import APP_URL, LOG
from lib.user import User
import os
import uuid

@pytest.fixture(scope="session")
def login_as_admin_token():
    LOG.info("login_as_admin_token")
    ADMIN_ACCOUNT = str(os.getenv("ADMIN_ACCOUNT"))
    ADMIN_PASSWORD = str(os.getenv("ADMIN_PASSWORD"))
    response = User().login(APP_URL, ADMIN_ACCOUNT, ADMIN_PASSWORD)
    assert response.ok

    access_token = response.json()["access_token"]
    yield access_token


@pytest.fixture(scope="function")
def test_temp_user_account(login_as_admin_token):
    LOG.info("login_as_admin_token")
    # step1: create an temp account
    LOG.info("Setting up a temp user account...")
    username = f"unique_name={uuid.uuid4().hex}"
    password = "testPassword"
    register_key = os.getenv("REGISTER_KEY")
    register_response = User().register(APP_URL, username, password, register_key)
    assert register_response.status_code == 201
    login_response = User().login(APP_URL, username, password)
    assert login_response.status_code == 201
    access_token = login_response.json()["access_token"]

    # step2: Find the temp_account's id.
    LOG.info(f"Get user's id...")
    response = User().user_list(APP_URL, login_as_admin_token)
    assert response.ok
    for user in response.json():
        if user["username"] == username:
            user_id = user["id"]
    assert isinstance(user_id, int)
    LOG.debug(f"username:{username}, id={user_id}")
    user_data = {
        "id":user_id,
        "username":username,
        "password":password,
        "access_token":access_token
    }


    yield user_data

    # step3. Delete the account after all the other processes are down.
    LOG.info("Delete the temp user account...")
    response = User().delete(APP_URL, login_as_admin_token, user_id)
    assert response.ok
    LOG.debug(f"username:{username}, is deleted.")