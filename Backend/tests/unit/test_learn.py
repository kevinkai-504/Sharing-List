from lib.learn import Learn
from config import APP_URL, LOG
from lib.utils import log_debug

def test_learn_post_db(temp_learn_item):
    learn_data = temp_learn_item
    LOG.debug(log_debug("db", "post", "learn", f"json = name:{learn_data["name"]}"))
    response_check = Learn().learn(APP_URL, learn_data["access_token"], learn_data["name"])
    assert response_check.status_code != 201
    LOG.debug(log_debug("db", "post", "learn", f"result = {response_check.json()}"))

