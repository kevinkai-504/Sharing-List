import pytest
from config import APP_URL, LOG, ADMIN_ACCOUNT, ADMIN_PASSWORD, REGISTER_KEY
from lib.user import User
from lib.learn import Learn
import uuid
from lib.utils import log_debug

@pytest.fixture(scope="session")
def login_as_admin_token():
    response = User().login(APP_URL, ADMIN_ACCOUNT, ADMIN_PASSWORD)
    assert response.ok
    access_token = response.json()["access_token"]

    yield access_token

    response = User().logout(APP_URL, access_token)
    assert response.ok

@pytest.fixture(scope="function")
def temp_user_account(login_as_admin_token):
    username = f"Unique_name={uuid.uuid4().hex}"
    password = "Password"
    register_key = REGISTER_KEY
    register_response = User().register(APP_URL, username, password, register_key)
    assert register_response.status_code == 201
    login_response = User().login(APP_URL, username, password)
    assert login_response.status_code == 201
    access_token = login_response.json()["access_token"]
    response = User().user_list(APP_URL, login_as_admin_token)
    assert response.ok
    for user in response.json():
        if user["username"] == username:
            user_id = user["id"]
    assert isinstance(user_id, int)
    user_data = {
        "id":user_id,
        "username":username,
        "password":password,
        "access_token":access_token
    }

    yield user_data

    response = User().logout(APP_URL, access_token)
    assert response.ok
    response = User().delete(APP_URL, login_as_admin_token, user_id)
    assert response.ok

@pytest.fixture(scope="function")
def temp_learn_item(temp_user_account):
    user_data = temp_user_account
    access_token = user_data["access_token"]
    learn_name = "learn_item"
    response = Learn().learn(APP_URL, access_token, learn_name)
    assert response.status_code == 201
    learn_data = response.json()
    learn_data["access_token"] = access_token

    yield learn_data

    response = Learn().delete(APP_URL, access_token, learn_data["id"])
    assert response.status_code == 200

    
