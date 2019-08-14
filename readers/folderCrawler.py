import os
import time
from readers.fileItem import FileItem
from readers.cacheFileHandler import CacheFileHandler

class FolderCrawler:

    # global vars to generate the index
    __total_scan_size = 0
    __total_files_list = dict()
    __stat_start_time = 0
    __stat_scan_size = 0
    __backup_start_time = 0

    root_dir = ""


    item_list = dict()
    cacheFileHandler = None

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.item_list = dict()
        self.cacheFileHandler = CacheFileHandler(root_dir)

    def run(self, use_cache = 1):

        # create the "current" kick starter item
        root_item = FileItem()
        root_item.create(self.root_dir, self.root_dir, '')

        # get the list from cache or start from fresh list
        if use_cache:
            self.item_list = self.cacheFileHandler.read_from_disc()
        else:
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
            current = FileItem()
            current.create(current_.root_dir, current_.dir, file_name)

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
            self.cacheFileHandler.write_to_disc(self.item_list)
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
            self.cacheFileHandler.write_to_disc(self.item_list)
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

