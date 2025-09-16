from lib.user import User
from config import APP_URL, LOG
import os
import uuid

def test_logout(test_temp_user_account):
    LOG.info("logout")
    response = User().logout(APP_URL, "fake_token")
    assert not response.ok
    access_token = test_temp_user_account["access_token"]
    response = User().logout(APP_URL, access_token)
    assert response.ok

def test_register_same_account(test_temp_user_account):
    LOG.info("register_same_account")
    exist_user_data = test_temp_user_account
    account = exist_user_data["username"]
    password = exist_user_data["password"]
    key = os.getenv("REGISTER_KEY")
    response = User().register(APP_URL, account, password, key)
    assert not response.ok

def test_resgister_wrong_key():
    LOG.info("resgister_wrong_key")
    account = str(uuid.uuid4())
    password = "testPassword"
    key = str(uuid.uuid4())
    response = User().register(APP_URL, account, password, key)
    assert not response.ok

# def test_NotAdmin_get_user_list(test_temp_user_account):

# def test_NotAdmin_delete_user(test_temp_user_account):



