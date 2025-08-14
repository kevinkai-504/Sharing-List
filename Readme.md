本專案目前僅供本地開發，尚未能夠線上部屬
後續將進行:資料庫容器化>線上部屬



開發者起始步驟:
    0. git init > git clone https://github.com/kevinkai-504/Sharing-List.git   >  cd到根目錄
    1. 將Backend>.env.example改成.env，並在裡面按指示輸入必須的環境變數
    2. (選擇性):由Backend>config.py可以自訂權限以決定管理者以及訪客
    3. 程式運行方法: (確認docker應用程式開啟)直接運行docker-compose up --build
    4. 前往本地網站: http://localhost:5173/?#