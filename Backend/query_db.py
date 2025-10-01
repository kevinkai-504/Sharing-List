from app import create_app
from models.learn import LearnModel
from models.user import UserModel
from config import ADMIN_ACCOUNT, ADMIN_PASSWORD
from db import db
from flask import jsonify
from passlib.hash import pbkdf2_sha256

app = create_app()

def query_learn_items():
    with app.app_context():
        print("正在連接資料庫...")
        
        # 這裡示範如何使用 filter_by 查詢 status 為 'A' 的學習項目
        # 您可以根據需要修改此處的查詢條件
        # learns = LearnModel.query.filter_by(status="A", name="HAHAHA").all()
        # print(len(learns))
        # if learns:
        #     print("查詢結果：")
        #     for learn in learns:
        #         print(f"ID: {learn.id}, 名稱: {learn.name}, 狀態: {learn.status}, 筆記: {learn.note}")
        # else:
        #     print("找不到符合條件的學習項目。")

        users = UserModel.query.all()
        if len(users) != 0:
            return
        user = UserModel(
            username=ADMIN_ACCOUNT,
            password=pbkdf2_sha256.hash(ADMIN_PASSWORD)
        )
        try:
            db.session.add(user)
            db.session.commit()
        except:
            print("something wrong")

        print("A initial account is ready!")




if __name__ == "__main__":
    query_learn_items()