from marshmallow import Schema, fields

class FileDirectory(object):
    def __init__(self, name: str, size: int, owner: int, permissions: str):
        self.name = name
        self.size = size
        self.owner = owner
        self.permissions = permissions

class FileDirectorySchema(Schema):
    name = fields.Str()
    size = fields.Integer()
    owner = fields.Integer()
    permissions =  fields.Str()