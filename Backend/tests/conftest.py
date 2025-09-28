import pytest
from config import APP_URL, ADMIN_ACCOUNT, ADMIN_PASSWORD, REGISTER_KEY, LOG
from lib.user import User
from lib.tag import Tag
from lib.learn import Learn
import uuid

@pytest.fixture(scope="session")
def login_as_admin_token():
    response = User().login(APP_URL, ADMIN_ACCOUNT, ADMIN_PASSWORD)
    assert response.ok
    access_token = response.json()["access_token"]

    check_amount_of_user_response = User().user_list(APP_URL, access_token)
    amount_of_user_before = len(check_amount_of_user_response.json())

    yield access_token

    check_amount_of_user_response = User().user_list(APP_URL, access_token)
    amount_of_user_after = len(check_amount_of_user_response.json())

    assert amount_of_user_before == amount_of_user_after
    
    LOG.debug(f"before = {amount_of_user_before}, after = {amount_of_user_after}")

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
    response = User().delete(APP_URL, login_as_admin_token, user_id)
    assert response.status_code != 200

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


@pytest.fixture(scope="function")
def get_learn_items(login_temp_account):
    data = login_temp_account
    access_token = data["access_token"]

    
    response = Tag().get_learn(APP_URL, access_token)
    assert response.json() == [] #測試功能與確認初始為空集合/learnFtag (post)
    response = Learn().post_learn(APP_URL, access_token, name="temp")
    assert response.ok #測試功能/learn (post)
    id = response.json()["id"]
    response = Learn().delete(APP_URL, access_token, id)
    assert response.ok #測試功能/learn/id (delete)


    response = Learn().post_learn(APP_URL, access_token, name="1")
    assert response.ok #建立1
    response = Learn().post_learn(APP_URL, access_token, name="2")
    assert response.ok #建立2
    response = Learn().post_learn(APP_URL, access_token, name="1、2")
    assert response.ok #建立1、2
    response = Learn().post_learn(APP_URL, access_token, name="else", note="else")
    assert response.ok #建立else且筆記紀錄else
    id_else = response.json()["id"]

    response = Learn().post_learn(APP_URL, access_token, name="else")
    assert not response.ok #確認不能同樣名稱建立 /learn (post)
    response = Learn().put(APP_URL, access_token, id_else, name="ELSE", status='A', note="else")
    assert response.ok #測試 /learn/id (put)
    response = Learn().put(APP_URL, access_token, id_else, name="1", status='A', note="else")
    assert not response.ok #確認不能改成已存在名稱 /learn/id (put)
    response = Learn().put(APP_URL, access_token, id_else, name="ELSE", status='A', note="ELSE")
    assert response.ok #測試 /learn/id (put)
    response = Learn().put(APP_URL, access_token, id_else, name="ELSE", status='B', note="ELSE")
    assert response.ok #測試 /learn/id (put)
    response = Learn().put(APP_URL, access_token, id_else, name="ELSE", status='B', note="ELSE")
    assert response.ok #確認沒有更改任何內容也能put成功 /learn/id (put)

    response = Tag().get_learn(APP_URL, access_token)
    assert response.ok

    data = {
        "learn_list":response.json(),
        "access_token":access_token
    }
    yield data


@pytest.fixture(scope="function")
def get_tag_items(get_learn_items):
    data = get_learn_items
    access_token = data["access_token"]
    response = Tag().get_all_tags(APP_URL, access_token)
    assert response.json() == [] #測試並確認初始tag_list是空集合 /tag (get)
    response = Tag().post_tag(APP_URL, access_token, name="1")
    assert response.ok #建立標籤1；測試 /tag (post)
    response = Tag().post_tag(APP_URL, access_token, name="2")
    assert response.ok #建立標籤2
    response = Tag().post_tag(APP_URL, access_token, name="else")
    assert response.ok #建立標籤else
    response = Tag().post_tag(APP_URL, access_token, name="else")
    assert not response.ok #確認tag不能重複建立 /tag (post)


    response = Tag().post_tag(APP_URL, access_token, name="del")
    assert response.ok #建立標籤del
    id_del = response.json()["id"]
    response = Tag().put_tag(APP_URL, access_token, name="delete", id=id_del)
    assert response.ok #測試 /tag/id (put)
    response = Tag().put_tag(APP_URL, access_token, name="delete", id=id_del)
    assert response.ok #確認put目前名稱的標籤沒問題 /tag/id (put)
    response = Tag().put_tag(APP_URL, access_token, name="else", id=id_del)
    assert not response.ok #確認put不能是已存在的標籤 /tag/id (put)
    response = Tag().delete_tag(APP_URL, access_token, id=id_del)
    assert response.ok #測試 /tag/id (delete)



    response = Tag().get_all_tags(APP_URL, access_token)
    assert response.ok
    yield response.json()
