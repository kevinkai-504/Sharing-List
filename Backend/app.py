from flask import Flask, jsonify
from flask_smorest import Api
from db import db
from flask_cors import CORS
from resources.learn import blp as LearnBlueprint
from resources.tag import blp as TagBlueprint

# 使用者登入
from flask_jwt_extended import JWTManager
from resources.user import blp as UserBlueprint
from datetime import timedelta
from config import expire_time_access
from blocklist import BLOCKLIST

# .env
import os

# 資料庫部屬用
from flask_migrate import Migrate





def create_app():
    app = Flask(__name__)

    # load_dotenv()   #0731新增匯入.env以處理os.getenv  #0811取消因為改由docker匯入環境

    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173').split(',')

    CORS(app, resources={r"/*": {"origins": CORS_ORIGINS}})
    app.config["API_TITLE"] = "Learns REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"

    # 新增swagger_UI方便展示與pytest建立
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = False

    db.init_app(app)
    api = Api(app)
    migrate = Migrate(app, db)  #資料庫部屬用

    # 使用者登入
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=expire_time_access)
    # app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=expire_time_refresh)
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "登入過久，請重新登入", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # @jwt.needs_fresh_token_loader
    # def token_not_fresh_callback(jwt_header, jwt_payload):
    #     return (
    #         jsonify(
    #             {
    #                 "message": "The token is not fresh.",
    #                 "error": "fresh_token_required",
    #             }
    #         ),
    #         401,
    #     )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )
    # 因為改用Migration所以不用
    # with app.app_context():
    #     import models

    #     db.create_all()

    api.register_blueprint(LearnBlueprint)
    api.register_blueprint(TagBlueprint)

    # 使用者登入
    api.register_blueprint(UserBlueprint) 


    return app