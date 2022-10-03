from marshmallow import Schema, fields, post_load

class UpdateFile(object):
    def __init__(self, filepath: str, owner: int, permissions: str, contents: str):
        self.filepath = filepath
        self.owner = owner
        self.permissions = permissions
        self.contents = contents

class UpdateFileSchema(Schema):
    filepath = fields.Str()
    owner = fields.Integer()
    permissions =  fields.Str()
    contents =  fields.Str()

    @post_load()
    def load_request(self, data, **kwargs):
        return UpdateFile(**data)