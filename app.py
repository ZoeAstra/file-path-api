import sys, os, stat, werkzeug
from shutil import rmtree
from flask import Flask, request
from models.directory import Directory
from models.file import File
from models.filecontents import FileContents, FileContentsSchema
from models.directorycontents import DirectoryContents, DirectoryContentsSchema
from models.error import Error, ErrorSchema

app = Flask(__name__, static_url_path='/static', static_folder='static')

root_dir = os.path.join(os.getcwd(), 'root')

@app.route('/api/', methods=["GET"])
@app.route('/api/<path:filepath>', methods=["GET"])
def get(filepath = ""):
    # basic check for existence - throw generic but helpful 400 error if it doesn't
    current_path = os.path.join(root_dir, filepath)
    if os.path.exists(current_path) == False:
        err_schema = ErrorSchema()
        return err_schema.dump(Error(400, 
                                    "Bad Request", 
                                    "Specified path does not exist")), 400
    
    # handle case of it being a directory
    if os.path.isdir(current_path):
        dir_list = os.listdir(current_path)
        file_list = []
        directory_list = []
        
        for file_sys_obj in dir_list:
            status = os.stat(os.path.join(current_path, file_sys_obj))

            if os.path.isfile(os.path.join(current_path, file_sys_obj)):
                file_list.append(File(file_sys_obj,
                                        status.st_size,
                                        str(status.st_uid),
                                        stat.filemode(status.st_mode)))

            if os.path.isdir(os.path.join(current_path, file_sys_obj)):
                directory_list.append(Directory(file_sys_obj,
                                                status.st_size,
                                                str(status.st_uid),
                                                stat.filemode(status.st_mode)))

        directory_contents_schema = DirectoryContentsSchema()
        return directory_contents_schema.dump(DirectoryContents(file_list, directory_list)), 200

    # case of it being a file 
    elif os.path.isfile(current_path):
        with open(current_path, 'r') as f:
            read_data = f.read()
        file_contents_schema = FileContentsSchema()
        status = os.stat(current_path)
        return file_contents_schema.dump(FileContents(os.path.basename(current_path),
                                                        status.st_size,
                                                        str(status.st_uid),
                                                        stat.filemode(status.st_mode),
                                                        read_data)), 200
    # don't know what else it could be, so throw 500 error, as something is clearly uhandled and it's probably our fault 
    else:
        err_schema = ErrorSchema()
        return err_schema.dump(Error(500, 
                                    "Internal Server Error", 
                                    "Unknown path/file type")), 500

@app.route('/api/<path:filepath>', methods=["DELETE"])
def delete(filepath = ""):
    # basic check for existence - throw generic but helpful 400 error if it doesn't
    current_path = os.path.join(root_dir, filepath)
    if os.path.exists(current_path) == False:
        err_schema = ErrorSchema()
        return err_schema.dump(Error(400, 
                                    "Bad Request", 
                                    "Specified path does not exist")), 400
    
    # handle case of it being a directory
    if os.path.isdir(current_path):
        rmtree(os.path.abspath(current_path))
        return "", 200

    # case of it being a file 
    elif os.path.isfile(current_path):
        os.remove(os.path.abspath(current_path))
        return "", 200
    # don't know what else it could be, so throw 500 error, as something is clearly uhandled and it's probably our fault 
    else:
        err_schema = ErrorSchema()
        return err_schema.dump(Error(500, 
                                    "Internal Server Error", 
                                    "Unknown path/file type")), 500

@app.route('/api/<path:filepath>', methods=["POST"])
def create(filepath = ""):
    # basic check for existence - throw generic but helpful 400 error if it doesn't
    current_path = os.path.join(root_dir, filepath)
    if os.path.exists(current_path) == True:
        err_schema = ErrorSchema()
        return err_schema.dump(Error(400, 
                                    "Bad Request", 
                                    "Path already exists")), 400
    
    # handle case of it being a directory
    if request.json["type"] == "directory":
        os.mkdir(os.path.abspath(current_path),un_filemode(request.json["permissions"]))
        return "", 200
    # case of it being a file 
    elif request.json["type"] == "file":
        with open(os.path.abspath(current_path), 'w') as f:
            f.write(request.json["contents"])
        return "", 200
    # don't know what else it could be, so throw 500 error, as something is clearly uhandled and it's probably our fault 
    else:
        err_schema = ErrorSchema()
        return err_schema.dump(Error(500, 
                                    "Internal Server Error", 
                                    "Unknown path/file type")), 500

@app.route('/api/<path:filepath>', methods=["PUT"])
def update(filepath = ""):
    # basic check for existence - throw generic but helpful 400 error if it doesn't
    current_path = os.path.join(root_dir, filepath)
    if os.path.exists(current_path) == False:
        err_schema = ErrorSchema()
        return err_schema.dump(Error(400, 
                                    "Bad Request", 
                                    "Specified path does not exist")), 400
    if request.json.get("filepath") != None:
        if os.path.exists(os.path.join(root_dir, request.json["filepath"])) == True:
            err_schema = ErrorSchema()
            return err_schema.dump(Error(400, 
                                        "Bad Request", 
                                        "New file/directory already exists")), 400
    new_path = os.path.join(root_dir, request.json.get("filepath"))

    # handle case of it being a directory
    if os.path.isdir(current_path):
        if request.json.get("contents") != None:
            err_schema = ErrorSchema()
            return err_schema.dump(Error(400, 
                                        "Bad Request", 
                                        "Malformed payload - 'contents' is a File-only PUT payload property")), 400
        # I don't know if chmod works in linux, as I am in windows and it doens't work here...
        os.chmod(os.path.abspath(current_path), un_filemode(request.json["permissions"]))
        os.rename(current_path, new_path)
        # os.chown(os.path.abspath(current_path), request.json["owner"])
        return "", 200

    # case of it being a file 
    elif os.path.isfile(current_path):
        os.chmod(os.path.abspath(current_path), 0o0777)
        with open(os.path.abspath(current_path), 'w') as f:
            f.write(request.json["contents"])
        os.chmod(os.path.abspath(current_path), un_filemode(request.json["permissions"]))
        os.rename(current_path, new_path)
        return "", 200
    # don't know what else it could be, so throw 500 error, as something is clearly uhandled and it's probably our fault 
    else:
        err_schema = ErrorSchema()
        return err_schema.dump(Error(500, 
                                    "Internal Server Error", 
                                    "Unknown path/file type")), 500

# I don't know if this works, as I am in windows...
def un_filemode(mode_str):
    filemode_table = (
        ((stat.S_IFLNK,         "l"),
        (stat.S_IFSOCK,        "s"),  # Must appear before IFREG and IFDIR as IFSOCK == IFREG | IFDIR
        (stat.S_IFREG,         "-"),
        (stat.S_IFBLK,         "b"),
        (stat.S_IFDIR,         "d"),
        (stat.S_IFCHR,         "c"),
        (stat.S_IFIFO,         "p")),

        ((stat.S_IRUSR,         "r"),),
        ((stat.S_IWUSR,         "w"),),
        ((stat.S_IXUSR|stat.S_ISUID, "s"),
        (stat.S_ISUID,         "S"),
        (stat.S_IXUSR,         "x")),

        ((stat.S_IRGRP,         "r"),),
        ((stat.S_IWGRP,         "w"),),
        ((stat.S_IXGRP|stat.S_ISGID, "s"),
        (stat.S_ISGID,         "S"),
        (stat.S_IXGRP,         "x")),

        ((stat.S_IROTH,         "r"),),
        ((stat.S_IWOTH,         "w"),),
        ((stat.S_IXOTH|stat.S_ISVTX, "t"),
        (stat.S_ISVTX,         "T"),
        (stat.S_IXOTH,         "x"))
    )
    mode = 0
    for char, table in zip(mode_str, stat._filemode_table):
        for bit, bitchar in table:
            if char == bitchar:
                mode |= bit
                break
    return mode

@app.errorhandler(werkzeug.exceptions.BadRequest)
@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_bad_request(e):
    err_schema = ErrorSchema()
    return err_schema.dump(Error(500, 
                                "Bad Request", 
                                "Unhandled Error")), 400

@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_internal_error(e):
    err_schema = ErrorSchema()
    return err_schema.dump(Error(500, 
                                "Internal Server Error", 
                                "Unhandled Error")), 500

if __name__ == '__main__':
    print (app.url_map)
    print (app.static_url_path)
    print (app.static_folder)
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    app.run(debug=True, use_reloader=True)
