import os
import json
import re
import datetime
import time
import glob
from readers.fileItem import FileItem
from readers.fileItem import FileItemEncoder


class CacheFileHandler:

    cache_folder = "cache"
    cache_ext = ".cache"
    root_dir = ""

    def __init__(self, root_dir):
        self.root_dir = root_dir

        return

    def write_to_disc(self, item_list):
        filename = self.__create_new_cache_file_name()

        print("filename: " + filename)

        json_str = FileItemEncoder().encode(item_list)
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
        for file_hash in item_list:
            count += 1
            total_size += item_list[file_hash].file_size

        print("count " + str(count) + " and size is " + str(total_size))

    def read_from_disc(self):

        latest_file = self.__get_latest_cache_file()
        print(latest_file)

        #
        with open(latest_file, 'r', encoding='utf8') as f:
            json_dict_array = json.load(f)

        # clear list
        item_list = dict()

        # bring the array alive to instances of class
        for key in json_dict_array:
            dict_item = json_dict_array[key]
            print(dict_item)
            inst = FileItem()
            inst.__dict__ = dict_item
            item_list[key] = inst

        return item_list

    def __get_cache_folder(self, make_sure_exists = 0):
        # get a clean filename
        sub_folder = re.sub('[^0-9a-zA-Z]+', '_', self.root_dir)
        cache_folder = os.path.join(self.cache_folder, sub_folder)
        if make_sure_exists:
            # make sure folders are created
            os.makedirs(cache_folder, exist_ok=True)

        return cache_folder

    def __create_new_cache_file_name(self):
        cache_folder = self.__get_cache_folder(True)
        # create a new timestamp
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S') + self.cache_ext
        # add the timestamp
        cache_file_name = os.path.join(cache_folder, timestamp)
        return cache_file_name

    def __get_all_cache_files(self):
        cache_folder = self.__get_cache_folder()

        # get all files in folder
        all_cache_files = glob.glob(os.path.join( cache_folder, '*' + self.cache_ext))
        return all_cache_files

    def __get_latest_cache_file(self):
        # get all cache files in folder
        file_list = self.__get_all_cache_files()
        # create a dict with modified timestamp
        all_cache_files = dict()
        for filename in file_list:
            last_mod_timestamp = os.path.getmtime(filename)
            all_cache_files[last_mod_timestamp] = filename
        # get the largest timestamp
        latest_timestamp = max(all_cache_files, key=float)
        # pick the item with largest timestamp
        latest_file = all_cache_files[latest_timestamp]
        return latest_file

