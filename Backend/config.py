admin = '1'  #管理者id(預設為第一個被創建的帳號就是管理者)
expire_time_access = 60 #min (設定token過期時間，預設60分鐘後過期)
guest = ['2','3']  #訪客的ID(預設第二個被創立的帳號只能看不能編輯;
# Backend>resources>user.py有開放管理者閱覽使用者ID，需自行下載如Insomnia等工具)

guest_mode = True #訪客模式開關(設False時就沒有區分訪客)


