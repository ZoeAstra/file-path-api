from typing import List
from marshmallow import Schema, fields
from .file import File, FileSchema
from .directory import Directory, DirectorySchema

class DirectoryContents(object):
    def __init__(self, files: List[File], directories: List[Directory]):
        self.files = files
        self.directories = directories

class DirectoryContentsSchema(Schema):
    files = fields.Nested(FileSchema, many=True)
    directories = fields.Nested(DirectorySchema, many=True)
