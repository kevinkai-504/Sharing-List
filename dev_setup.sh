#!/bin/sh

echo "正在啟動 Docker 服務..."
docker-compose up --build -d

echo "等待後端服務啟動..."
sleep 20 # 根據您的機器效能調整等待時間，確保服務已啟動

echo "初始化 Flask-Migrate..."
docker-compose exec backend flask db init

echo "生成初始 Migration 腳本..."
docker-compose exec backend flask db migrate -m "Initial migration"

echo "完成專案設定，您現在可以使用您的應用程式了。"