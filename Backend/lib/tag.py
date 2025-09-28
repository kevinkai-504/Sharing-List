from lib.utils import build_request_headers
from config import SESSION

class Tag:
    def __init__(self):
        self.learn = "/learnFtag"
        self.tag_list = []

        self.tag = "/tag"
    def get_learn(self, app_url, access_token):
        payload = {"tag_list":self.tag_list}
        request_header = build_request_headers(access_token)
        response = SESSION.post(f"{app_url}{self.learn}", headers=request_header, json=payload)
        return response
    
    def get_all_tags(self, app_url, access_token):
        request_header = build_request_headers(access_token)
        response = SESSION.get(f"{app_url}{self.tag}", headers=request_header)
        return response
    
    def post_tag(self, app_url, access_token, name):
        request_header = build_request_headers(access_token)
        payload = {"name":name}
        response = SESSION.post(f"{app_url}{self.tag}", headers=request_header, json=payload)
        return response
    
    def put_tag(self, app_url, access_token, id, name):
        request_header = build_request_headers(access_token)
        payload = {"name":name}
        response = SESSION.put(f"{app_url}{self.tag}/{id}", headers=request_header, json=payload)
        return response
    def delete_tag(self, app_url, access_token, id):
        request_header = build_request_headers(access_token)
        response = SESSION.delete(f"{app_url}{self.tag}/{id}", headers=request_header)
        return response