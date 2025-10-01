2025/9/5:已部屬(https://sharing-list-frontend.onrender.com)
2025/10/1:新增CI/CD(Pytest、Makefile、Github Action)

預計於10/2前增加使用範例與參考資源
--------------------

開發者步驟(本地):
    0. 確認有安裝git與docker(Make推薦安裝)

    1. 進Backend>.env.example改成.env，並詳閱參數設定內容(不修正也可執行)

    2. 於Terminal輸入Make build即可運行；可透過Make test測試功能正常與否

    3. 前往本地網站: http://localhost:5173

開發者步驟(CICD):
    0. 於github action增加secret key。詳見.github>workflows>main.yml與.env.example。預設push main時觸發

開發者步驟(部屬):
    0. 以Render當作部屬平台，部屬db、Backend、Frontend三個伺服器，部屬方法如下:
    
    1.1 部屬db: 選PostgreSQL。
    其他設定照常，最後得到Internal Database URL

    1.2 部屬Backend:選Web Service>指定後端git repo，且環境語言是Docker。環境變數見Backend>.env.example。
    其他照常設定，最後得到後端網址

    1.3 部屬Frontend:選擇static site>指定前端git repo>Build Command填寫:npm install && npm run build。
    其他照常設定，最後得到前端網址
    
    2.1 Backend環境參數:CORS_ORIGINS、APP_URL更新成實際參數

    2.2 Frontend環境參數:新增VITE_API_URL，value為Backend的實際網址

    3. 進入Frontend網址即可運行
