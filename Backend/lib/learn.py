from lib.utils import build_request_headers
from config import SESSION, LOG

class Learn:
    def __init__(self):
        self.learn_url = "/learn"
    def learn(self, app_url, access_token, name):
        request_header = build_request_headers(access_token)
        payload = {"name":name, "note":""}
        response = SESSION.post(f"{app_url}{self.learn_url}", headers=request_header, json=payload)
        return response
    def delete(self, app_url, access_token, learn_id):
        request_header = build_request_headers(access_token)
        response = SESSION.delete(f"{app_url}{self.learn_url}/{learn_id}", headers=request_header)
        return response