from .filedirectory import FileDirectory, FileDirectorySchema
from marshmallow import post_load

class Directory(FileDirectory):
    def __init__(self,name:str,size:int,owner:int,permissions:str):
        super().__init__(name, size, owner, permissions)

class DirectorySchema(FileDirectorySchema):
    @post_load
    def make_directory(self, data, **kwargs):
        return Directory(**data)
