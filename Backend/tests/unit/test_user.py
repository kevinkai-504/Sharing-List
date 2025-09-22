from lib.user import User
from config import APP_URL, LOG, REGISTER_KEY, SESSION
import uuid
from lib.utils import log_debug
import uuid


# /register
def test_register_func(create_temp_account):
    data = create_temp_account
    LOG.debug(log_debug("register_func", "post", "register", f"payload = username:{data["username"]}, password:{data["password"]}, register_key:{REGISTER_KEY}, result = {data["response"]}"))

def test_register_secu_same_username(create_temp_account):
    exist_user_data = create_temp_account
    username = exist_user_data["username"]
    password = exist_user_data["password"]
    register_key = REGISTER_KEY
    LOG.debug(log_debug("register_secu_same_username", "post", "register", f'payload = username:{username}, password:{password}, register_key:{register_key}'))
    response = User().register(APP_URL, username, password, register_key)
    assert not response.ok
    LOG.debug(log_debug("register_secu_same_username", "post", "register", f'result={response.json()}'))

def test_resgister_secu_wrong_key():
    username = uuid.uuid4().hex
    password = uuid.uuid4().hex
    register_key = uuid.uuid4().hex
    LOG.debug(log_debug("resgister_secu_wrong_key", "post", "register", f'payload = username:{username}, password:{password}, register_key:{register_key}'))
    response = User().register(APP_URL, username, password, register_key)
    assert not response.ok
    LOG.debug(log_debug("resgister_secu_wrong_key", "post", "register", f'result={response.json()}'))


# /login
def test_login_func(login_temp_account):
    data = login_temp_account
    LOG.debug("login_func", "post", "login", f"payload & access_token = {data}")

def test_login_secu_wrong_password(login_temp_account):
    exist_user_data = login_temp_account
    username = exist_user_data["username"]
    password = uuid.uuid4().hex()
    LOG.debug("login_secu_wrong_password", "post", "login", f"payload = username:{username}, password:{password}")
    response = User().login(APP_URL, username, password)
    assert response.status_code != 201
    LOG.debug(log_debug("login_secu_wrong_password", "post", "login", f'result={response.json()}'))

def test_login_secu_wrong_username(login_temp_account):
    exist_user_data = login_temp_account
    username = uuid.uuid4().hex()
    password = exist_user_data["password"]
    LOG.debug("login_secu_wrong_username", "post", "login", f"payload = username:{username}, password:{password}")
    response = User().login(APP_URL, username, password)
    assert response.status_code != 201
    LOG.debug(log_debug("login_secu_wrong_username", "post", "login", f'result={response.json()}'))

def test_login_secu_Nonregister():
    username = uuid.uuid4().hex()
    password = uuid.uuid4().hex()
    LOG.debug("login_secu_Nonregister", "post", "login", f"payload = username:{username}, password:{password}")
    response = User().login(APP_URL, username, password)
    assert response.status_code != 201
    LOG.debug(log_debug("login_secu_Nonregister", "post", "login", f'result={response.json()}'))


# /logout
def test_logout_func(create_temp_account):
    data = create_temp_account
    username = data["username"]
    password = data["password"]
    login_response = User().login(APP_URL, username, password)
    assert login_response.status_code == 201
    access_token = login_response.json()["access_token"]
    LOG.debug("logout_func", "post", "logout", f"header = {access_token}")
    response = User().logout(APP_URL, access_token)
    assert response.ok
    LOG.debug("logout_func", "post", "logout", f"result = {response.json()}")

def test_logout_secu_wrong_token():
    access_token = uuid.uuid4().hex()
    LOG.debug("logout_secu_wrong_token", "post", "logout", f"header = {access_token}")
    response = User().logout(APP_URL, access_token)
    assert not response.ok
    LOG.debug("logout_secu_wrong_token", "post", "logout", f"result = {response.json()}")

def test_logout_secu_old_token(create_temp_account):
    data = create_temp_account
    username = data["username"]
    password = data["password"]
    login_response = User().login(APP_URL, username, password)
    assert login_response.status_code == 201
    access_token = login_response.json()["access_token"]
    LOG.debug("logout_secu_old_token", "post", "logout", f"header = {access_token}")
    response = User().logout(APP_URL, access_token)
    assert response.ok
    response = User().logout(APP_URL, access_token)
    assert not response.ok
    LOG.debug("logout_secu_old_token", "post", "logout", f"result = {response.json()}")


# /user
def test_get_users_func(get_temp_account):
    LOG.debug("get_users_func", "get", "user", "begin&result = {get_temp_account}")

def test_get_users_secu_notAdmin(login_temp_account):
    data = login_temp_account
    access_token = data["access_token"]
    LOG.debug("get_users_func", "get", "user")
    response = User().user_list(APP_URL, access_token)
    assert response.status_code != 200
    LOG.debug("get_users_func", "get", "user", f"result = {response.json()}")

# /user/id
def test_delete_user_func(login_as_admin_token, get_temp_account):
    temp_user_id = get_temp_account["id"]
    temp_user_username = get_temp_account["username"]
    LOG.debug("delete_user_func", "delete", "user/id", f"target_name and id = {get_temp_account}")
    response = User().delete(APP_URL, login_as_admin_token, temp_user_id)
    assert response.status_code == 200

    response_check = User().user_list(APP_URL, login_as_admin_token)
    assert response_check.status_code == 200
    username_should_not_exist = ""
    for user in response_check.json():
        if user["username"] == temp_user_username:
            username_should_not_exist = temp_user_username
    assert username_should_not_exist == ""
    LOG.debug("delete_user_func", "delete", "user/id", f"target_name and id = {get_temp_account}")

# def test_delete_user_secu_not_Admin(get_temp_account):
    









