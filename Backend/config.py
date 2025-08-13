admin = '1'  #管理者id(預設為第一個被創建的帳號就是管理者)
expire_time_access = 60 #min (設定token過期時間，預設60分鐘後過期)
guest = '2'  #訪客id(預設第二個被創立的帳號只能看不能編輯)
guest_mode = True #訪客模式開關(設False即會取消訪客不能編輯的限制)


#管理者額外路由見Backend>resources>user.py


