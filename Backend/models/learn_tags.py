from db import db


class LearnsTags(db.Model):
    __tablename__ = "learns_tags"

    id = db.Column(db.Integer, primary_key=True)
    learn_id = db.Column(db.Integer, db.ForeignKey("learns.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
