from config import LOG, APP_URL
from lib.utils import log_debug
from lib.learn import Learn
from lib.tag import Tag
from lib.user import User


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
    response = Tag().get_link(APP_URL, access_token=None, learn_id=999, tag_id=999)
    assert response.json()['error'] == "authorization_required"
    response = Tag().post_link(APP_URL, access_token=None, learn_id=999, tag_id=999)
    assert response.json()['error'] == "authorization_required"
    response = Tag().delete_link(APP_URL, access_token=None, learn_id=999, tag_id=999)
    assert response.json()['error'] == "authorization_required"

def test_guest_behave(initial_guest):
    access_token = initial_guest
    if access_token == "None":
        return

    response = Learn().post_learn(APP_URL, access_token, name="temp")
    assert not response.ok
    response = Learn().delete(APP_URL, access_token, learn_id=999)
    assert not response.ok
    response = Learn().put(APP_URL, access_token, learn_id=999, name="ELSE", status='A', note="else")
    assert not response.ok

    response = Tag().get_learn(APP_URL, access_token) #允許訪客看到項目列表
    assert response.ok
    response = Tag().get_all_tags(APP_URL, access_token) #允許訪客看到所有標籤
    assert response.ok
    response = Tag().post_tag(APP_URL, access_token, name="1")
    assert not response.ok
    response = Tag().put_tag(APP_URL, access_token, name="delete", id=999)
    assert not response.ok
    response = Tag().delete_tag(APP_URL, access_token, id=999)
    assert not response.ok
    response = Tag().get_link(APP_URL, access_token, learn_id=999, tag_id=999)
    assert not response.ok
    response = Tag().post_link(APP_URL, access_token, learn_id=999, tag_id=999)
    assert not response.ok
    response = Tag().delete_link(APP_URL, access_token, learn_id=999, tag_id=999)
    assert not response.ok
