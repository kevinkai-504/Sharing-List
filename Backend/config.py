import requests
import logging
import os

admin = os.getenv("ADMIN").split(",")  #管理者id(預設為第一個被創建的帳號就是管理者)
guest = os.getenv("GUEST").split(",")  #訪客的ID(預設第二個被創立的帳號只能看不能編輯;
guest_mode = bool(os.getenv("GUEST_MODE")) #訪客模式開關(設False時就沒有區分訪客)
expire_time_access = 60 #min (設定token過期時間，預設60分鐘後過期)

# Pytest
SESSION = requests.Session()
APP_URL = os.environ.get('APP_URL', 'http://127.0.0.1:5000')
ADMIN_ACCOUNT = os.getenv("ADMIN_ACCOUNT")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

LOG = logging.getLogger()
class HideSensitiveData(logging.Filter):
    def filter(self, record):
        record.msg = str(record.msg).replace(ADMIN_PASSWORD, "********")
        return True
LOG.addFilter(HideSensitiveData())

