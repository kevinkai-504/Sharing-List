from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from models import LearnModel
from schemas import LearnSchema, LearnUpdateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import datetime

from flask_jwt_extended import (
    jwt_required,
)
from lib.utils import Sub, integrityCheck
now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')


blp = Blueprint("learns", __name__, description="Control Learning Items")
@blp.route("/learn/<int:learn_id>")
class Learn(MethodView):
    @blp.arguments(LearnUpdateSchema)
    @blp.response(200, LearnSchema)
    @jwt_required()
    def put(self, learn_data, learn_id):
        learn = LearnModel.query.get(learn_id)
        Sub(learn.user_id)
        if learn_data["status"].upper() not in ["A", "B", "C", "D"]:
            abort(400, message="You should type A~D.")
        try:
            learn.name = learn_data["name"]
            learn.status = learn_data["status"].upper()
            learn.note = learn_data["note"]
            
            learns = LearnModel.query.filter_by(user_id=int(Sub()), name=learn_data["name"]).all()
            integrityCheck(learns, "put")

            db.session.add(learn)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred updating learns.")
               
        return learn
    
    @jwt_required()
    def delete(self, learn_id):
        learn = LearnModel.query.get_or_404(learn_id)
        Sub(learn.user_id)
        db.session.delete(learn)
        db.session.commit()
        return jsonify({"message": "Learn Item deleted!"}), 200

   
@blp.route("/learn")
class LearnList(MethodView):
    #有標籤時，此get暫時由tag.py進行
    # @jwt_required()
    # @blp.response(200, LearnSchema(many=True))
    # def get(self):
    #     return LearnModel.query.filter_by(user_id=int(Sub())).all()

    @blp.arguments(LearnSchema)
    @blp.response(201, LearnSchema)
    @jwt_required()
    def post(self, learn_data):
        learn = LearnModel(name=learn_data["name"], note=learn_data["note"], status="A", build_time=now, user_id=int(Sub()))
        learns = LearnModel.query.filter_by(user_id=int(Sub()), name=learn_data["name"]).all()
        integrityCheck(learns, "post")
        try:
            db.session.add(learn)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the learn.")
        return learn
    





