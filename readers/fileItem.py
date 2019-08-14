import os
import hashlib
from json import JSONEncoder


class FileItem:

    # global base folder
    root_dir = ""

    # rel path -- path relative to root
    rel_path = ""

    # current crawl directory (root + rel)
    dir = ""

    # filename
    file_name = ""

    # full path (root + dir + filename)
    full_path = ""

    # timestamp of file
    last_mod_timestamp = 0

    # file size
    file_size = 0

    # dict hash -- hash that identifies unique rel_path
    dict_hash = ""

    # content hash
    md5sum = ""

    def __init__(self):

        return

    def create(self, root_dir, current_dir, filename):
        self.root_dir = root_dir
        self.dir = current_dir
        self.file_name = filename

        # Create all information needed
        self.full_path = os.path.join(self.dir, self.file_name)
        self.rel_path = os.path.relpath(self.full_path, self.root_dir)
        self.dict_hash = self.__get_name_hash()

        # this works only on real files
        if os.path.exists(self.full_path):
            self.last_mod_timestamp = os.path.getmtime(self.full_path)
            st = os.stat(self.full_path)
            self.file_size = st.st_size

        # update dir
        if self.is_directory():
            self.dir = self.full_path

    def is_sym_link(self):
        if os.path.islink(self.full_path):
            return 1
        else:
            return 0

    def is_directory(self):
        if os.path.isdir(self.full_path):
            return 1
        else:
            return 0

    # this function is processing expensive - call only if really needed
    def create_content_hash(self):
        hash_md5 = hashlib.md5()
        with open(self.full_path, "rb") as f:
            for chunk in iter(lambda: f.read(4*1024*1024), b""):
                hash_md5.update(chunk)
        self.md5sum = hash_md5.hexdigest()

    def __get_name_hash(self):
        hash_md5 = hashlib.md5()
        hash_md5.update(self.rel_path.encode('utf-8'))
        return hash_md5.hexdigest()

    # for serializing
    def obj_dict(self):
        return self.__dict__


class FileItemEncoder(JSONEncoder):

    def default(self, obj):

        if isinstance(obj, FileItem):

            return obj.__dict__
