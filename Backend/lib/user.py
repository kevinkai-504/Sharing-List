from lib.utils import build_request_headers
from config import SESSION, LOG

class User:
    def __init__(self):
        self.login_url = "/login"
        self.logout_url = "/logout"
        self.resgister_url = "/register"
    def login(self, app_url, username, password):
        LOG.info("login")
        payload = {"username":username, "password":password}
        response = SESSION.post(f"{app_url}{self.login_url}", json=payload)
        return response
    
    def logout(self, app_url, access_token):
        requtest_headers = build_request_headers(access_token)
        response = SESSION.post(f"{app_url}{self.logout_url}", headers=requtest_headers)
        return response
    
    def register(self, app_url, username, password, key):
        payload = {"username":username, "password":password, "key":key}
        response = SESSION.post(f"{app_url}{self.resgister_url}", json=payload)
        return response
