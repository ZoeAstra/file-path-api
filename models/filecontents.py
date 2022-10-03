from .file import File, FileSchema
from marshmallow import fields

class FileContents(File):
    def __init__(self,name:str,size:int,owner:int,permissions:str,contents:str):
        super().__init__(name, size, owner, permissions)
        self.contents = contents
    
class FileContentsSchema(FileSchema):
    contents = fields.String()
