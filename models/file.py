from marshmallow import post_load
from .filedirectory import FileDirectory, FileDirectorySchema

class File(FileDirectory):
    def __init__(self,name:str,size:int,owner:int,permissions:str):
        super().__init__(name, size, owner, permissions)

class FileSchema(FileDirectorySchema):
    @post_load
    def make_file(self, data, **kwargs):
        return File(**data)
