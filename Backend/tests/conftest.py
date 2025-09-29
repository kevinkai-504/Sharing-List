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
    id_1 = response.json()["id"]
    response = Learn().post_learn(APP_URL, access_token, name="2")
    assert response.ok #建立2
    id_2 = response.json()["id"]
    response = Learn().post_learn(APP_URL, access_token, name="1、2")
    assert response.ok #建立1、2
    id_12 = response.json()["id"]
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
        "access_token":access_token,
        "learn_id_list":{"id_1":id_1, "id_2":id_2, "id_12":id_12, "id_else":id_else}
    }
    yield data


@pytest.fixture(scope="function")
def get_tag_items(get_learn_items):
    data = get_learn_items
    access_token = data["access_token"]
    learn_id_list = data["learn_id_list"]

    response = Tag().get_all_tags(APP_URL, access_token)
    assert response.json() == [] #測試並確認初始tag_list是空集合 /tag (get)
    response = Tag().post_tag(APP_URL, access_token, name="1")
    assert response.ok #建立標籤1；測試 /tag (post)
    t_id_1 = response.json()["id"]
    response = Tag().post_tag(APP_URL, access_token, name="2")
    assert response.ok #建立標籤2
    t_id_2 = response.json()["id"]
    response = Tag().post_tag(APP_URL, access_token, name="else")
    assert response.ok #建立標籤else
    t_id_else = response.json()["id"]
    response = Tag().post_tag(APP_URL, access_token, name="else")
    assert not response.ok #確認tag不能重複建立 /tag (post)

    tag_id_list = {"id_1":t_id_1, "id_2":t_id_2, "id_else":t_id_else}

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

    response = Tag().get_link(APP_URL, access_token, learn_id=learn_id_list["id_1"], tag_id=tag_id_list["id_1"])
    assert response.json()["message"] == "The Link is not exist." #測試與確認初始狀態下沒有鍵結關係 /learn/learn_id/tag/tag_id (post)
    response = Tag().post_link(APP_URL, access_token, learn_id=learn_id_list["id_1"], tag_id=tag_id_list["id_1"])
    assert response.ok #測試&建立關係 /learn/learn_id/tag/tag_id (post)
    response = Tag().get_link(APP_URL, access_token, learn_id=learn_id_list["id_1"], tag_id=tag_id_list["id_1"])
    assert response.ok #確認建立關係後能get到關係 /learn/learn_id/tag/tag_id (get)

    # 建立其他對應連結
    response = Tag().post_link(APP_URL, access_token, learn_id=learn_id_list["id_2"], tag_id=tag_id_list["id_2"])
    assert response.ok
    response = Tag().post_link(APP_URL, access_token, learn_id=learn_id_list["id_12"], tag_id=tag_id_list["id_1"])
    assert response.ok
    response = Tag().post_link(APP_URL, access_token, learn_id=learn_id_list["id_12"], tag_id=tag_id_list["id_2"])
    assert response.ok
    response = Tag().post_link(APP_URL, access_token, learn_id=learn_id_list["id_else"], tag_id=tag_id_list["id_else"])
    assert response.ok

    # 確認標籤是否正確篩選項目 /learnFtag (post)
    response = Tag().get_learn(APP_URL, access_token, tag_list=[tag_id_list["id_1"]])
    assert len(response.json()) == 2
    assert set([response.json()[0]["id"], response.json()[1]["id"]]) == set([learn_id_list["id_1"], learn_id_list["id_12"]])
    response = Tag().get_learn(APP_URL, access_token, tag_list=[tag_id_list["id_2"]])
    assert len(response.json()) == 2
    assert set([response.json()[0]["id"], response.json()[1]["id"]]) == set([learn_id_list["id_2"], learn_id_list["id_12"]])
    response = Tag().get_learn(APP_URL, access_token, tag_list=[tag_id_list["id_else"]])
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == learn_id_list["id_else"]
    response = Tag().get_learn(APP_URL, access_token, tag_list=[tag_id_list["id_1"], tag_id_list["id_2"]])
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == learn_id_list["id_12"]
    response = Tag().get_learn(APP_URL, access_token, tag_list=[tag_id_list["id_1"], tag_id_list["id_2"], tag_id_list["id_else"]])
    assert response.ok
    assert len(response.json()) == 0
    response = Tag().get_learn(APP_URL, access_token, tag_list=[tag_id_list["id_1"], tag_id_list["id_else"]])
    assert response.ok
    assert len(response.json()) == 0

    # 確認有存在連結的標籤不能被刪除 /tag/id (delete)
    response = Tag().delete_tag(APP_URL, access_token, id=tag_id_list["id_else"])
    assert not response.ok
    assert response.json()['message'] == "Tag is linking with learn item."

    response = Tag().delete_link(APP_URL, access_token, learn_id=learn_id_list["id_else"], tag_id=tag_id_list["id_else"])
    assert response.ok #測試 /learn/learn_id/tag/tag_id (delete)
    response = Tag().delete_tag(APP_URL, access_token, id=tag_id_list["id_else"])
    assert response.ok #確認不存在連結的標籤可以被刪除


    # 確認假如項目被刪掉的話之後該連結的tag會自動取消連結，且假如該tag沒有任何其他連結就可以成功被刪除 /tag/id (delete)
    response = Tag().post_tag(APP_URL, access_token, name="else")
    assert response.ok
    tag_id = response.json()["id"]
    response = Tag().post_link(APP_URL, access_token, learn_id=learn_id_list["id_else"], tag_id=tag_id)
    assert response.ok
    response = Learn().delete(APP_URL, access_token, learn_id_list["id_else"])
    assert response.ok
    response = Tag().delete_tag(APP_URL, access_token, id=tag_id)
    assert response.ok


    response = Tag().get_all_tags(APP_URL, access_token)
    assert response.ok
    yield response.json()
