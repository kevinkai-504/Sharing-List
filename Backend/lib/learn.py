import requests
from lib.utils import build_request_headers

class Learn:
    def __init__(self):
        self.learn_url = "/learn"
    def get_all_learns(self, app_url, access_token):
        request_header = build_request_headers(access_token)
        response = requests.get(f"{app_url}{self.learn_url}", headers=request_header)
        return response