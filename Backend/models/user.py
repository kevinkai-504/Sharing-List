from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)


    # 使用者連動
    learns = db.relationship("LearnModel", back_populates="user", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="user", lazy="dynamic", cascade="all, delete")

