from lib.utils import build_request_headers
from config import SESSION, LOG

class Learn:
    def __init__(self):
        self.learn_url = "/learnFtag"
        self.learn_url_2 = "/learn"
    def get_all_learns(self, app_url, access_token):
        request_header = build_request_headers(access_token)
        response = SESSION.get(f"{app_url}{self.learn_url}", headers=request_header)
        LOG.debug(response.json())
        return response