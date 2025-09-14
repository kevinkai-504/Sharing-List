from flask_smorest import abort
from config import guest, guest_mode

def build_request_headers(access_token, content_type="application/json"):
    headers = {
        "Authorization":f"Bearer {access_token}",
        "Accept": content_type
    }
    return headers

def check_guest(sub):
    if sub in guest and guest_mode is True:
        abort(401, message="You are a guest!")