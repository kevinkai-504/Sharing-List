from flask_smorest import abort
from config import guest, guest_mode, admin
from flask_jwt_extended import get_jwt

def build_request_headers(access_token, content_type="application/json"):
    headers = {
        "Authorization":f"Bearer {access_token}",
        "Accept": content_type
    }
    return headers

# def check_guest(sub): #後來全部改成Sub來產生sub與自動檢查
#     if sub in guest and guest_mode is True:
#         abort(401, message="You are a guest!")


class Sub:
    def __init__(self, *target_id, admin_mode=False):
        self.sub = get_jwt()['sub']
        self.target_id = target_id
        self.admin_mode = admin_mode

        self._check()
    def __int__(self):
        return int(self.sub)
    def _check(self):
        if self.sub in guest and guest_mode is True:
            abort(401, message="You are a guest!")
        if self.admin_mode == True and self.sub not in admin:
            abort(401, message="You are not the administrator!")
        if self.target_id and int(self.sub) not in self.target_id:
            abort(401, message="You are not the user!")
    

def integrityCheck(items):
    if len(items) > 0:
        abort(400, message="The item's name already exists.")