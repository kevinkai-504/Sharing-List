2025/9/5:已部屬(https://sharing-list-frontend.onrender.com)

預計9月底前新增CI/CD(Pytest、Makefile、Github Action)、增加使用範例(訪客帳號開放)、增加參考資源(於訪客帳號登入頁面說明)
--------------------

開發者步驟(本地):
    0. 確認有安裝git與docker

    1. 進Frontend>vite-project/src>Config.jsx，改成"url_default":"http://127.0.0.1:5000"

    2. 進Backend>.env.example改成.env；填入ADMIN_ACCOUNT與ADMIN_PASSWORD

    3. (選擇性).env內參數自行參閱與設定

    4. 程式運行方法: 根目錄運行docker compose up --build啟用服務、docker compose down停止服務

    5. 前往本地網站: http://localhost:5173

    6. (選擇性)有下載Make的話可於Makefilet查看快速指令，裡面包含pytest測試(有按照上述操作與啟用服務時，輸入make test應可測試成功)

開發者步驟(部屬):
    0. (以Render作為部屬網站，可直接連結github repo)
    
    1.1 部屬db: 選PostgreSQL。
    其他設定照常，最後得到Internal Database URL

    1.2 部屬後端:選Web Service>指定後端git repo，且環境語言是Docker。環境變數見Backend>.env.example。
    其他照常設定，最後得到後端網址

    1.3 部屬前端:選擇static site>指定前端git repo>Build Command填寫:npm install && npm run build。
    其他照常設定，最後得到前端網址

    2. 進Frontend>vite-project/src>Config.jsx，確認設定"url_default":"http://127.0.0.1:5000"改為部屬成功得到的後端網址
    

    3. 重新修改後端的環境參數CORS_ORIGINS改成剛得到的前端網址，且APP_URL輸入後端網址後，即可運行
