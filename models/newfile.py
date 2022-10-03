from marshmallow import Schema, fields, post_load

class NewFile(object):
    def __init__(self, owner: int, permissions: str, contents: str):
        self.owner = owner
        self.permissions = permissions
        self.contents = contents
        self.type = "file"

class NewFileSchema(Schema):
    owner = fields.Integer()
    permissions =  fields.Str()
    contents =  fields.Str()
    type = fields.Str()

    @post_load()
    def load_request(self, data, **kwargs):
        return NewFile(**data)