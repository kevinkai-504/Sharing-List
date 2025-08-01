from marshmallow import fields, Schema


class PlainLearnSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    status = fields.Str()
    note = fields.Str()
    build_time = fields.Str(dump_only=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class LearnUpdateSchema(Schema):
    name = fields.Str()
    status = fields.Str()
    note = fields.Str()

class LearnSchema(PlainLearnSchema):
    tag = fields.List(fields.Nested(PlainTagSchema()))
    user_id = fields.Int(dump_only=True) #使用者連動

class TagSchema(PlainTagSchema):
    learn = fields.List(fields.Nested(PlainLearnSchema()), dump_only=True)
    user_id = fields.Int(dump_only=True) #使用者連動

class TagFilterSchema(Schema):
    tag_list = fields.List(fields.Int, load_only=True)

class LearnAndTagSchema(Schema):
    learn = fields.Nested(LearnSchema(), dump_only=True)
    tag = fields.Nested(TagSchema(), dump_only=True)


# 驗證
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    learns = fields.List(fields.Nested(PlainLearnSchema()), dump_only=True)  #使用者連動
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)     #使用者連動

# 授權碼
class UserFirstTimeSchema(UserSchema):
    key = fields.Str(required=True, load_only=True)








