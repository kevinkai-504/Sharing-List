from lib.user import User
from config import APP_URL, LOG, REGISTER_KEY
import uuid
from lib.utils import log_debug

def test_register_same_account(test_temp_user_account):
    LOG.info("\nregister_same_account")

    exist_user_data = test_temp_user_account
    account = exist_user_data["username"]
    password = exist_user_data["password"]
    key = REGISTER_KEY
    LOG.debug(log_debug("secu", "post", "register", f'JSON = username:{account}, password:{password}, register_key:{key}'))
    response = User().register(APP_URL, account, password, key)
    assert not response.ok
    LOG.debug(log_debug("secu", "post", "register", f'result={response.json()}'))

def test_resgister_wrong_key():
    LOG.info("\nresgister_wrong_key")

    account = str(uuid.uuid4())
    password = "testPassword"
    key = str(uuid.uuid4())
    LOG.debug(log_debug("secu", "post", "register", f'JSON = username:{account}, password:{password}, register_key:{key}'))
    response = User().register(APP_URL, account, password, key)
    assert not response.ok
    LOG.debug(log_debug("secu", "post", "register", f'result={response.json()}'))



