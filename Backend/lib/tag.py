from lib.utils import build_request_headers
from config import SESSION, LOG

class Tag:
    def __init__(self):
        self.learn = "/learnFtag"
        self.tag_list = []
    def get_learn(self, app_url, access_token):
        payload = {"tag_list":self.tag_list}
        request_header = build_request_headers(access_token)
        response = SESSION.post(f"{app_url}{self.learn}", headers=request_header, json=payload)
        return response