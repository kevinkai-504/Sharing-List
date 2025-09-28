from config import LOG, APP_URL
from lib.utils import log_debug
from lib.learn import Learn
from lib.tag import Tag


# learn所有method但不包含tag測試
def test_learns_without_tag_func(get_learn_items):
    data = get_learn_items
    LOG.debug(data["learn_list"])

# tags
def test_tags(get_tag_items):
    LOG.debug(get_tag_items)


def test_Plainlearns_not_token():
    LOG.debug("learns_not_token")
    response = Learn().post_learn(APP_URL, access_token=None, name="temp")
    assert response.json()['error'] == "authorization_required"
    response = Learn().delete(APP_URL, access_token=None, learn_id=999)
    assert response.json()['error'] == "authorization_required"
    response = Learn().put(APP_URL, access_token=None, learn_id=999, name="ELSE", status='A', note="else")
    assert response.json()['error'] == "authorization_required"

def test_Plaintags_not_token():
    response = Tag().get_learn(APP_URL, access_token=None)
    assert response.json()['error'] == "authorization_required"
    response = Tag().get_all_tags(APP_URL, access_token=None)
    assert response.json()['error'] == "authorization_required"
    response = Tag().post_tag(APP_URL, access_token=None, name="1")
    assert response.json()['error'] == "authorization_required"
    response = Tag().put_tag(APP_URL, access_token=None, name="delete", id=999)
    assert response.json()['error'] == "authorization_required"
    response = Tag().delete_tag(APP_URL, access_token=None, id=999)
    assert response.json()['error'] == "authorization_required"
