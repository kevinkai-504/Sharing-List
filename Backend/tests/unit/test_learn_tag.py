from config import LOG
from lib.utils import log_debug


# learn所有method但不包含tag測試
def test_learns_without_tag_func(get_learn_items):
    data = get_learn_items
    LOG.debug(data["learn_list"])

# tags
def test_tags(get_tag_items):
    LOG.debug(get_tag_items)


