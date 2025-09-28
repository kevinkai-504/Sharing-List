from lib.tag import Tag
from config import APP_URL, LOG, REGISTER_KEY
from lib.utils import log_debug


# /learnFtag
def test_learnFtag_func(get_learn_items):
    data = get_learn_items
    assert data
    LOG.debug(data)