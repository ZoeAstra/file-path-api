from models.file import File, FileSchema
from models.directory import Directory, DirectorySchema
from models.newfile import NewFile, NewFileSchema
from models.updatefile import UpdateFile, UpdateFileSchema
from models.error import Error, ErrorSchema
import requests

def test_root():
  r = requests.get("http://localhost:5000/api/")
  assert r.status_code == 200
  assert r.text == """{"directories":[{"name":"testfolder","owner":5678,"permissions":"drwxr-xr-x","size":4096},{"name":"filedir","owner":5678,"permissions":"drwxr-xr-x","size":4096}],"files":[{"name":"testfile.txt","owner":5678,"permissions":"-rwxr-xr-x","size":45}]}
"""

def test_file():
  r = requests.get("http://localhost:5000/api/testfile.txt")
  assert r.status_code == 200
  assert r.text == """{"contents":"hi, this is a test file\\ntesting 1...2...3...","name":"testfile.txt","owner":5678,"permissions":"-rwxr-xr-x","size":45}
"""

def test_multiple_directories():
  r = requests.get("http://localhost:5000/api/testfolder")
  assert r.status_code == 200
  assert r.text == """{"directories":[{"name":"pulvinar","owner":5678,"permissions":"drwxr-xr-x","size":4096},{"name":"loremipsum","owner":5678,"permissions":"drwxr-xr-x","size":4096}],"files":[{"name":"testfile2.txt","owner":5678,"permissions":"-rwxr-xr-x","size":32}]}
"""

def test_multiple_files():
  r = requests.get("http://localhost:5000/api/testfolder/loremipsum")
  assert r.status_code == 200
  assert r.text == """{"directories":[],"files":[{"name":"lorem2.txt","owner":5678,"permissions":"-rwxr-xr-x","size":714},{"name":"lorem.txt","owner":5678,"permissions":"-rwxr-xr-x","size":451}]}
"""

def test_post_file():
  nf_schema = NewFileSchema()
  r = requests.post("http://localhost:5000/api/test.txt", data = nf_schema.dump(NewFile(0, "-rwxr-xr-x", "test file")))
  print(nf_schema.dump(NewFile(0, "-rwxr-xr-x", "test file")))
  assert r.status_code == 200
  
def test_put_file():
  uf_schema = UpdateFileSchema()
  r = requests.put("http://localhost:5000/api/test.txt", data = uf_schema.dump(UpdateFile("test2.txt", 0, "-rwxr-xr-x", "test file 123")))
  assert r.status_code == 200

def test_delete_file():
  r = requests.delete("http://localhost:5000/api/test2.txt")
  assert r.status_code == 200