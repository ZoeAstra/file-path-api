from marshmallow import Schema, fields, post_load

class Error(object):
    def __init__(self, status: int, message: str, detail: str):
        self.status = status
        self.message = message
        self.detail = detail

class ErrorSchema(Schema):
    status = fields.Integer()
    message =  fields.Str()
    detail =  fields.Str()
    @post_load()
    def load_error(self, data, **kwargs):
        return Error(**data)