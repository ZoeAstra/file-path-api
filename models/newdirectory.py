from marshmallow import Schema, fields, post_load

class NewDirectory(object):
    def __init__(self, owner: int, permissions: str):
        self.owner = owner
        self.permissions = permissions
        self.type = "Directory"

class NewDirectorySchema(Schema):
    owner = fields.Integer()
    permissions =  fields.Str()
    type = fields.Str()

    @post_load()
    def load_request(self, data, **kwargs):
        return NewDirectory(**data)