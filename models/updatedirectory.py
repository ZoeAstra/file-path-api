from marshmallow import Schema, fields, post_load

class UpdateDirectory(object):
    def __init__(self, filepath:str, owner: int, permissions: str):
        self.filepath = filepath
        self.owner = owner
        self.permissions = permissions

class UpdateDirectorySchema(Schema):
    filepath = fields.Str()
    owner = fields.Integer()
    permissions =  fields.Str()

    @post_load()
    def load_request(self, data, **kwargs):
        return UpdateDirectory(**data)