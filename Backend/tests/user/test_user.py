from lib.user import User
from config import APP_URL, LOG
import os
import uuid

def test_logout(login_as_admin_token):
    LOG.info("logout")
    access_token = login_as_admin_token
    response = User().logout(APP_URL, access_token)
    assert response.ok

def test_register():
    LOG.info("register")

    LOG.info("register-Test if same account can not be created.")
    account = os.getenv("ADMIN_ACCOUNT")
    password = os.getenv("ADMIN_PASSWORD")
    key = os.getenv("REGISTER_KEY")
    response = User().register(APP_URL, account, password, key)
    assert not response.ok

    LOG.info("register-Test if wrong key can prevent from creating new account.")
    account = str(uuid.uuid4())
    password = "123"
    key = str(uuid.uuid4())
    response = User().register(APP_URL, account, password, key)
    assert not response.ok

    LOG.info("register-Test if can create an account.")
    account = str(uuid.uuid4())
    password = "123"
    key = os.getenv("REGISTER_KEY")
    response = User().register(APP_URL, account, password, key)
    msg = response.json()
    LOG.debug(msg)
    assert response.ok

