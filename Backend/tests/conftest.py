import pytest
from config import APP_URL, LOG, ADMIN_ACCOUNT, ADMIN_PASSWORD, REGISTER_KEY
from lib.user import User
import uuid
from lib.utils import log_debug

@pytest.fixture(scope="session")
def login_as_admin_token():
    LOG.info("\n(fixture-session)login_as_admin_token")
    response = User().login(APP_URL, ADMIN_ACCOUNT, ADMIN_PASSWORD)
    assert response.ok
    access_token = response.json()["access_token"]


    yield access_token
    LOG.info("\n(fixture-session)login_as_admin_token - end")


    LOG.debug(log_debug("func", "post", "logout", f"Set target token"))
    response = User().logout(APP_URL, access_token)
    assert response.ok
    response_check = User().logout(APP_URL, access_token)
    assert not response_check.ok
    LOG.debug(log_debug("func", "post", "logout", f"result = {response.json()}"))

@pytest.fixture(scope="function")
def test_temp_user_account(login_as_admin_token):
    LOG.info("\n(fixture-fucntion)temp_user_account")
    username = f"Unique_name={uuid.uuid4().hex}"
    password = "Password"
    register_key = REGISTER_KEY
    LOG.debug(log_debug("func", "post", "register", f'JSON = username:{username}, password:{password}, register_key:{register_key}'))
    register_response = User().register(APP_URL, username, password, register_key)
    assert register_response.status_code == 201
    LOG.debug(log_debug("func", "post", "register", f"result = {register_response.json()}"))


    LOG.debug(log_debug("func", "post", "login", f'JSON = username:{username}, password:{password}'))
    login_response = User().login(APP_URL, username, password)
    assert login_response.status_code == 201
    access_token = login_response.json()["access_token"]
    LOG.debug(log_debug("func", "post", "login", f'Success! Get a temp token with username:{username}.'))


    LOG.debug(log_debug("func", "get", "user"))
    response = User().user_list(APP_URL, login_as_admin_token)
    assert response.ok
    for user in response.json():
        if user["username"] == username:
            user_id = user["id"]
    assert isinstance(user_id, int)
    LOG.debug(log_debug("func", "get", "user", f"result = username:{username}, it's id={user_id}"))

    user_data = {
        "id":user_id,
        "username":username,
        "password":password,
        "access_token":access_token
    }


    yield user_data
    LOG.info("\n(fixture-function)temp_user_account - end")
    response = User().logout(APP_URL, access_token)
    assert response.ok


    LOG.debug(log_debug("func", "delete", "user/<user_id>", f"id={user_id}"))
    response = User().delete(APP_URL, login_as_admin_token, user_id)
    assert response.ok
    response = User().user_list(APP_URL, login_as_admin_token)
    assert response.ok
    for user in response.json():
        assert user["username"] != username
    LOG.debug(log_debug("func", "delete", "user/<user_id>", f"Success!"))
