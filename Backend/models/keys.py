from db import db


class KeyModel(db.Model):
    __tablename__ = "keys"

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
