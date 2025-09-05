本專案目前僅供本地開發，尚未能夠線上部屬
後續將進行:資料庫容器化>線上部屬
--------------------
2025/9/5:已部屬(https://sharing-list-frontend.onrender.com/)

下期預計新增CI/CD與修改部分文字敘述
--------------------

開發者步驟(本地測試):
    0. 確認有安裝git與docker

    1. 進Frontend>vite-project/src>Config.jsx，改成"url_default":"http://127.0.0.1:5000"

    2. 進Backend>.env.example改成.env，並確認授權碼以利後續帳號註冊(可自訂)

    3. (選擇性):由Backend>config.py可以自訂權限以決定管理者以及訪客

    4. 程式運行方法: 根目錄運行docker-compose up --build
    5. 前往本地網站: http://localhost:5173/

開發者步驟(部屬用):
    0. (以Render作為部屬網站)
    
    1.1 部屬db: 選PostgreSQL。
    其他設定照常，最後得到Internal Database URL

    1.2 部屬後端:選Web Service>指定後端git repo，且環境語言是Docker。環境變數見Backend>.env.example。
    其他照常設定，最後得到後端網址

    1.3 部屬前端:選擇static site>指定前端git repo>Build Command填寫:npm install && npm run build。
    其他照常設定，最後得到前端網址

    2. 進Frontend>vite-project/src>Config.jsx，確認設定"url_default":"http://127.0.0.1:5000"改為部屬成功得到的後端網址

    3. 重新修改後端的環境參數CORS_ORIGINS改成剛得到的前端網址，即可運行