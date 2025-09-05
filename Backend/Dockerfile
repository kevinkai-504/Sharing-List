FROM python:3.12
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .  
RUN pip install -r requirements.txt
COPY . .
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--reload", "run:app"]
# 取消上述CMD為了避免在資料庫出現前就開啟服務
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["/bin/sh", "./docker-entrypoint.sh"]