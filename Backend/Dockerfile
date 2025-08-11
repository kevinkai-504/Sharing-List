FROM python:3.12
EXPOSE 5000
WORKDIR /Backend
RUN pip install -r requirements.txt
COPY . .
CMD ["python","run.py","--host","0.0.0.0"]