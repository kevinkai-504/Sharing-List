from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from models import TagModel, LearnModel, LearnsTags
from schemas import TagSchema, LearnAndTagSchema, LearnSchema, TagFilterSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from flask_jwt_extended import jwt_required
from lib.utils import Sub, integrityCheck


blp = Blueprint("tags", __name__, description="Control tags")
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def put(self, tag_data, tag_id):
        tag = TagModel.query.get(tag_id)
        Sub(tag.user_id)
        try:
            tag.name = tag_data["name"]
            tags = TagModel.query.filter_by(user_id=int(Sub()), name=tag_data["name"]).all()
            integrityCheck(tags, "put")
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, messgae="An error occurred updating tags.")
        return tag
    
    @jwt_required()
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        Sub(tag.user_id)
        if not tag.learn:
            db.session.delete(tag)
            db.session.commit()
            return jsonify({"message": "Tag Item deleted!"}), 200
        abort(
            400,
            message="Tag is linking with learn item."
        )


@blp.route("/tag")
class TagList(MethodView):
    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data):
        tag = TagModel(**tag_data, user_id=int(Sub()))
        tags = TagModel.query.filter_by(user_id=int(Sub()), name=tag_data["name"]).all()
        integrityCheck(tags, "post")
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")
        return tag
   
    @jwt_required()
    @blp.response(200, TagSchema(many=True))
    def get(self):
        return TagModel.query.filter_by(user_id=int(Sub())).all()
   
@blp.route("/learn/<int:learn_id>/tag/<int:tag_id>")
class LinkLearnToTag(MethodView):
    @jwt_required()
    @blp.response(201, TagSchema)
    def post(self, learn_id, tag_id):
        learn = LearnModel.query.get_or_404(learn_id)
        tag = TagModel.query.get_or_404(tag_id)
        Sub(learn.user_id, tag.user_id)
        learn.tag.append(tag)

        try:
            db.session.add(learn)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while linking between tag and learn item.")
        return tag
   
    @jwt_required()
    @blp.response(200, LearnAndTagSchema)
    def delete(self, learn_id, tag_id):
        learn = LearnModel.query.get_or_404(learn_id)
        tag = TagModel.query.get_or_404(tag_id)
        Sub(learn.user_id, tag.user_id)
        learn.tag.remove(tag)

        try:
            db.session.add(learn)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting link between learn and tag item.")
        return tag
   
    @jwt_required()
    @blp.response(200, LearnAndTagSchema)
    def get(self, learn_id, tag_id):
        try:
            if LearnsTags.query.filter_by(learn_id=learn_id, tag_id=tag_id).all():
                return jsonify({"message":"true"}), 200
            return jsonify({"message":"The Link is not exist."}), 404
        except SQLAlchemyError:
            abort(500, message="An error occurred while checking link between learn and tag item.")

       
@blp.route("/learnFtag")
class LearList_TagFilter(MethodView):
    @jwt_required()
    @blp.arguments(TagFilterSchema)
    @blp.response(201, LearnSchema(many=True))
    def post(self, tag_list):
        if tag_list["tag_list"] == []:
            return LearnModel.query.filter_by(user_id=int(Sub())).all()

        learn_id_set = set()
        learn_id_array = []
        learn_list = []

        for tag_id in tag_list["tag_list"]:
            Sub(TagModel.query.get_or_404(tag_id).user_id)
        
        tag = TagModel.query.get_or_404(tag_list["tag_list"][0])
        learns = tag.learn
        for learn in learns:
            learn_id_set.add(learn.id)

        for tag in tag_list["tag_list"][1:]:
            learn_id_array = []
            tag = TagModel.query.get_or_404(tag)
            learns = tag.learn
            for learn in learns:
                learn_id_array.append(learn.id)
            learn_id_set = learn_id_set.intersection(learn_id_array)
            
        for learn_id in list(learn_id_set):
            learn_list.append(LearnModel.query.get_or_404(learn_id))
        return learn_list

           
