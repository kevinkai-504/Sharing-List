from db import db

class LearnModel(db.Model):
    __tablename__ = "learns"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=False, nullable=False)

    status = db.Column(db.String(1), unique=False)

    tag = db.relationship("TagModel", secondary="learns_tags", back_populates="learn")

    note = db.Column(db.String(128))

    build_time = db.Column(db.String(64), nullable=False)


    # 使用者連動
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    user = db.relationship("UserModel", back_populates="learns")

