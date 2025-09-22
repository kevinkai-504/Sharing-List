import pytest
from config import APP_URL, LOG, ADMIN_ACCOUNT, ADMIN_PASSWORD, REGISTER_KEY
from lib.user import User
from lib.learn import Learn
import uuid

@pytest.fixture(scope="session")
def login_as_admin_token():
    response = User().login(APP_URL, ADMIN_ACCOUNT, ADMIN_PASSWORD)
    assert response.ok
    access_token = response.json()["access_token"]

    yield access_token

    response = User().logout(APP_URL, access_token)
    assert response.ok

@pytest.fixture(scope="function")
def create_temp_account(login_as_admin_token):
    username = f"Unique_name={uuid.uuid4().hex}"
    password = f"Unique_password={uuid.uuid4().hex}"
    register_response = User().register(APP_URL, username, password, REGISTER_KEY)
    assert register_response.status_code == 201
    data = {"username":username, "password":password, "response":register_response.json()}

    yield data

    response = User().user_list(APP_URL, login_as_admin_token)
    assert response.status_code == 200
    for user in response.json():
        if user["username"] == username:
            user_id = user["id"]
    response = User().delete(APP_URL, login_as_admin_token, user_id)
    assert response.status_code == 200

@pytest.fixture(scope="function")
def login_temp_account(create_temp_account):
    data = create_temp_account
    username = data["username"]
    password = data["password"]
    login_response = User().login(APP_URL, username, password)
    assert login_response.status_code == 201
    data = {"username":username, "password":password, "access_token":login_response.json()["access_token"]}

    yield data

    logout_response = User().logout(APP_URL, data["access_token"])
    assert logout_response.ok
    
@pytest.fixture(scope="function")
def get_temp_account(login_as_admin_token, login_temp_account):
    data_temp_account = login_temp_account
    temp_uername = data_temp_account["username"]
    response = User().user_list(APP_URL, login_as_admin_token)
    assert response.status_code == 200
    for user in response.json():
        if user["username"] == temp_uername:
            temp_user_id = user["id"]
    assert temp_user_id
    data = {"username":temp_uername, "id":temp_user_id}

    yield data


# @pytest.fixture(scope="function")
# def user_factory(login_as_admin_token):
#     created_users = []
#     def create_user(num):
#         for _ in num:
#             username = f"Unique_name={uuid.uuid4().hex}"
#             password = f"Unique_password={uuid.uuid4().hex}"
#             register_response = User().register(APP_URL, username, password, REGISTER_KEY)
#             assert register_response.status_code == 201
#             data = {"username":username, "password":password, "response":register_response.json()}
#             created_users.append(data)
#         return data
#     create_user(2)

#     yield created_users

#     for user in created_users:
#         response = User().user_list(APP_URL, login_as_admin_token)
#         assert response.status_code == 200
#         for user in response.json():
#             if user["username"] == :
#                 user_id = user["id"]
#         response = User().delete(APP_URL, login_as_admin_token, user_id)
#         assert response.status_code == 200



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

    
