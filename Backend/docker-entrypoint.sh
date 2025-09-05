#!/bin/sh

# 在啟動 gunicorn 之前執行資料庫遷移
flask db upgrade

# 啟動 gunicorn 伺服器
exec gunicorn --bind 0.0.0.0:5000 "run:app"