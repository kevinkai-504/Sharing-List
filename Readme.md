本專案目前僅供本地開發，尚未能夠線上部屬
後續將進行:資料庫容器化>線上部屬



開發者起始步驟:
    1. 將Backend>.env.example改成.env，並在裡面按指示輸入必須的環境變數
    2. (選擇性):由Backend>config.py可以自訂權限
    3. (選擇性):如要自己進行docker多次運行，請將.gitignore中的data.db移除，以免資料每次都遺失
    4. 程式運行方法: 於目標資料夾的終端bash輸入: docker-compose up --build
    5. 前往本地網站: http://localhost:5173/?#