#!/bin/sh

# 在啟動 gunicorn 之前執行資料庫遷移
flask db upgrade

# 判斷是否須建立初始使用者
python /app/query_db.py

# 啟動 gunicorn 伺服器
exec gunicorn --bind 0.0.0.0:5000 --reload "run:app"