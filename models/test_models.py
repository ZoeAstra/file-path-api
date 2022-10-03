from .file import File
from .filecontents import FileContents
from .directory import Directory
from .directorycontents import DirectoryContents


def test_create_directory_contents():
    # new_file = FileContents("file.txt",50,1,"-rwxr-xr-x","testing testing 123")
    new_directory_contents = DirectoryContents([File("file.txt",50,1,"-rwxr-xr-x"),
                                                File("file2.txt",50,3,"-rwxr-xr-x")],
                                                [Directory("directory",0,1,"drwxrwxrwx"),
                                                Directory("directory2",0,2,"drwxrwxrwx"),
                                                Directory("directory3",0,1,"drwxrwxrwx")])
    assert len(new_directory_contents.directories) == 3
    assert len(new_directory_contents.files) == 2

def test_create_file():
    new_file = File("file.txt",50,1,"-rwxr-xr-x")
    assert new_file.name == "file.txt"
    assert new_file.size == 50
    assert new_file.owner == 1
    assert new_file.permissions == "-rwxr-xr-x"

def test_create_file_contents():
    new_file = FileContents("file.txt",50,1,"-rwxr-xr-x","testing testing 123")
    assert new_file.name == "file.txt"
    assert new_file.size == 50
    assert new_file.owner == 1
    assert new_file.permissions == "-rwxr-xr-x"
    assert new_file.contents == "testing testing 123"

def test_create_directory():
    new_dir = Directory("directory",5,1,"drwxrwxrwx")
    assert new_dir.name == "directory"
    assert new_dir.size == 5
    assert new_dir.owner == 1
    assert new_dir.permissions == "drwxrwxrwx"