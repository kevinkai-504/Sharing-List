from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import UserModel
from schemas import UserSchema, UserFirstTimeSchema, CommentSchema

# 使用者登入
from passlib.hash import pbkdf2_sha256
from blocklist import BLOCKLIST
from config import admin
from flask_jwt_extended import (
    create_access_token,
    # create_refresh_token,
    # get_jwt_identity,
    get_jwt,
    jwt_required,
)
import os
from lib.utils import Sub
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("Users", __name__, description="Operations on users")





@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserFirstTimeSchema)
    def post(self, user_data):
        if user_data["key"] != os.getenv("REGISTER_KEY"):
            return jsonify({"message":"Invalid!"}), 401
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            return jsonify({"message":"A user with that username already exists."}), 409
        
        
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]) 
        )
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return jsonify({"message":"something wrong"})

        return jsonify({"message":"User successfully created!"}), 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id))
            # refresh_token = create_refresh_token(str(user.id))  之後有refresh需求再加
            return jsonify({"access_token":access_token}), 201
        
        return jsonify({"message":"Invalid!"}), 401


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return jsonify({"message":"Successfully logged out."}), 200

# 等之後有refresh需求再加
# @blp.route("/refresh")
# class TokenRefresh(MethodView):
#     @jwt_required(refresh=True)
#     def post(self):
#         current_user = get_jwt_identity()
#         new_token = create_access_token(identity=current_user, fresh=False)
#         jti = get_jwt()["jti"]
#         BLOCKLIST.add(jti)
#         return jsonify({"access_token":new_token}), 200
    

# 此段僅供管理者使用
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    def delete(self, user_id):
        Sub(admin_mode=True)
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":"User deleted."}), 200

# 此段僅供管理者使用
@blp.route("/user")
class UserList(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        Sub(admin_mode=True)
        user = UserModel.query.all()
        return user
    
@blp.route("/usercomment/<int:user_id>")
class UserComment(MethodView):
    @jwt_required()
    @blp.arguments(CommentSchema)
    @blp.response(200, CommentSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get(user_id)
        Sub()
        try:
            user.comment = user_data['comment']
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred when editing comment.")
        return {'comment':user.comment}
    
    @jwt_required()
    @blp.response(200, CommentSchema)
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        Sub(allow=True)
        return {'comment':user.comment}
        


