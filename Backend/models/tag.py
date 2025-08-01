from db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=False, nullable=False)
    learn = db.relationship("LearnModel", secondary="learns_tags", back_populates="tag")


    # 使用者連動
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    user = db.relationship("UserModel", back_populates="tags")
