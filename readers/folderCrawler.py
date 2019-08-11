import os
import time
import hashlib
import json
import re
from json import JSONEncoder
import datetime


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

    def __init__(self, root_dir, current_dir):
        self.root_dir = root_dir
        self.dir = current_dir

    def update_name(self, file_item):
        self.file_name = file_item

        # Create all information needed
        self.full_path = os.path.join(self.dir, self.file_name)
        self.rel_path = os.path.relpath(self.full_path, self.root_dir)
        self.last_mod_timestamp = os.path.getmtime(self.full_path)
        st = os.stat(self.full_path)
        self.file_size = st.st_size
        self.dict_hash = self.__get_name_hash()

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

    def default(self, object):

        if isinstance(object, FileItem):

            return object.__dict__


class FolderCrawler:

    # global vars to generate the index -- \TODO: find a better way of doing that
    __total_scan_size = 0
    __total_files_list = dict()
    __stat_start_time = 0
    __stat_scan_size = 0
    __backup_start_time = 0

    root_dir = ""

    cache_folder = "cache"
    cache_ext = ".cache"
    
    item_list = dict()

    def __init__(self, root_dir):
        self.root_dir = root_dir

    def run(self):

        # create the "current" kick starter item
        root_item = FileItem(self.root_dir, self.root_dir)

        # list of all indexed files from last run (will be used to speed-up indexing)
        self.item_list = dict()

        # start crawling
        self.__run_recursive(root_item)

        print("--- index done ---")

    def __run_recursive(self, current_):

        # create a list of files and sub directory names in the given directory
        list_of_files = os.listdir(current_.dir)

        # Iterate over all the entries (files, folders, sym_links, ... )
        for file_name in list_of_files:

            # create a copy and start crawling the subdir
            current = FileItem(current_.root_dir, current_.dir)

            # set file item
            current.update_name(file_name)

            # check for sym links
            if current.is_sym_link():
                print("skipping symlink " + current.full_path)
                continue

            # If entry is a directory then get the list of files in this directory
            if current.is_directory():
                # go to sub folders
                self.__run_recursive(current)
                continue

            # check if the same file already been indexed in the partly index
            if self.__is_modified_file(current) == 1:

                # creating the md5sum over the complete file is processing expensive
                current.create_content_hash()

                # add current FileItem to list
                self.item_list[current.dict_hash] = current

            # store the current result as temporary result -- just in case something goes wrong, we can continue later
            self.__stats_and_backup(current)

        # check if all files are parsed
        if current_.dir == self.root_dir:
            # force write
            self.__write_to_disc()
            print("\r\n" + "finished writing to disc")

        return

    def __is_modified_file(self, file_item):

        dict_hash = file_item.dict_hash

        if dict_hash in self.item_list:
            existing_file_item = self.item_list[dict_hash]
            # check the details
            if existing_file_item.file_size != file_item.file_size:
                return 1
            if existing_file_item.last_mod_timestamp != file_item.last_mod_timestamp:
                return 1

            return 0
        else:
            # not yet in list, treat like modified
            return 1

    def __stats_and_backup(self, current, force=0):

        self.__backup_to_disk(current, force)

        self.__display_stats(current, force)


    def __backup_to_disk(self, current, force = 0):

        if self.__backup_start_time == 0:
            self.__backup_start_time = time.time()

        backup_delta_time = time.time() - self.__backup_start_time
        if backup_delta_time > 60:
            # reset timer
            self.__backup_start_time = time.time()
            # execute backup
            self.__write_to_disc()
            #__writeIndexFile(rootDir, iname, __total_files_list, ts, __PARTLY)
            #__writeIndexFile(rootDir, iname, __total_files_list, ts, __PARTLY + ".dual")
            print("\nautomatic backup of index done\n")


    def __display_stats(self, current, force = 0):

        if self.__stat_start_time == 0:
            self.__stat_start_time = time.time()

        # stats
        self.__total_scan_size += current.file_size
        self.__stat_scan_size += current.file_size

        # the write timer
        delta_time = (time.time() - self.__stat_start_time)

        # on timer threshold
        if (delta_time > 1) or (force == 1):
            # reset timer
            self.__stat_start_time = time.time()

            # debug output
            size_in_mb = self.__stat_scan_size / 1024 / 1024
            throughput = size_in_mb / delta_time
            # reset byte counter
            self.__stat_scan_size = 0
            relname = current.rel_path
            debug = "[files: {f:5d},  size: {s:8.2f}MB {t:8.2f}MB/s] [{x:60}]".format(f=len(self.item_list),
                                                                                      s=self.__total_scan_size / 1024 / 1024,
                                                                                      t=throughput, x=relname)
            print("\r" + debug, end="\r")

    def __get_cache_file(self):
        # get a clean filename
        sub_folder = re.sub('[^0-9a-zA-Z]+', '_', self.root_dir)
        cache_folder = os.path.join(self.cache_folder, sub_folder)
        # make sure folders are created
        os.makedirs(cache_folder, exist_ok=True)
        # create a new timestamp
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S') + self.cache_ext
        # add the timestamp
        cache_file_name = os.path.join(cache_folder, timestamp)
        return cache_file_name


    def __write_to_disc(self):
        filename = self.__get_cache_file()

        print("filename: " + filename)

        json_str = FileItemEncoder().encode(self.item_list)
        # print(jsonStr)

        # beautify
        json_obj = json.loads(json_str)
        json_str = json.dumps(json_obj, indent=2)

        # actually write to file
        with open(filename, 'w', encoding='utf8') as outfile:
            outfile.write(json_str)

        # some stats output
        count = 0
        total_size = 0
        for file_hash in self.item_list:
            count += 1
            total_size += self.item_list[file_hash].file_size

        print("count " + str(count) + " and size is " + str(total_size))