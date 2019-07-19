import os
import time
import hashlib


class FileItem:

    # global base folder
    root_dir = ""

    # current crawl directory (root + rel)
    dir = ""

    # rel path -- path relative to root
    rel_path = ""

    # full path (root + dir + filename)
    full_path = ""

    # timestamp of file
    last_mod_timestamp = 0

    # file size
    file_size = 0

    # dict hash -- hash that identifies unique rel_path
    dict_hash = ""

    def __init__(self, root_dir, current_dir):
        self.root_dir = root_dir
        self.dir = current_dir

    def update_name(self, file_item):
        # Create all information needed
        self.full_path = os.path.join(self.dir, file_item)
        self.rel_path = os.path.relpath(self.full_path, self.root_dir)
        self.last_mod_timestamp = os.path.getmtime(self.full_path)
        st = os.stat(self.full_path)
        self.file_size = st.st_size
        self.dict_hash = self.__get_name_hash()

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

    def __get_name_hash(self):
        hash_md5 = hashlib.md5()
        hash_md5.update(self.rel_path.encode('utf-8'))
        return hash_md5.hexdigest()


class FolderCrawler:

    # global vars to generate the index -- \TODO: find a better way of doing that
    __total_scan_size = 0
    __total_files_list = dict()
    __stat_start_time = 0
    __stat_scan_size = 0
    __backup_start_time = 0

    def run(self, root_dir):

        # create the "current" item
        current = FileItem(root_dir)

        self.__run_recursive(current)

    def __run_recursive(self, current_, iname, ts):

        # create a copy and start crawling the subdir
        current = FileItem(current_.root_dir, current_.dir)

        # create a list of file and sub directories
        # names in the given directory
        list_of_files = os.listdir(current.dir)

        if self.__stat_start_time == 0:
            self.__stat_start_time = time.time()

        if self.__backup_start_time == 0:
            self.__backup_start_time = time.time()

        # Iterate over all the entries (files, folders, sym_links, ... )
        for file_name in list_of_files:

            # set file item
            current.update_name(file_name)

            # check for sym links
            if current.is_sym_link():
                print("skipping symlink " + current.full_path)
                continue

            # If entry is a directory then get the list of files in this directory
            if current.is_directory():
                # go to sub folders
                self.__run_recursive(current, iname, ts)
                continue

            # check if the same file already been indexed in the partly index
            sameEntry = __isSameFile(__total_files_list, relpath, fsize, lastModTimeStamp)
            if sameEntry == 0:
                # file is not yet present in index -- so add to index

                # creating the md5sum over the complete file is processing expensive
                md5sum = __md5(fullPath)
                # generate the tuple
                tuple = {"fname": entry, "fsize": fsize, "lastmod": lastModTimeStamp, "md5": md5sum,
                         "rootname": rootDir, "rname": relpath}
                # add to dict
                __total_files_list[dictHash] = tuple

                # store the current result as temporary result -- just in case something goes wrong, we can continue
            backupDeltaTime = time.time() - __backup_start_time
            if backupDeltaTime > 60:
                # reset timer
                __backup_start_time = time.time()
                # execute backup
                __writeIndexFile(rootDir, iname, __total_files_list, ts, __PARTLY)
                __writeIndexFile(rootDir, iname, __total_files_list, ts, __PARTLY + ".dual")
                print("automatic backup of index done")

            # stats
            __total_scan_size += fsize
            __stat_scan_size += fsize

            # the write timer
            deltaTime = (time.time() - __stat_start_time)

            # on timer threshold
            if deltaTime > 1:
                # reset timer
                __stat_start_time = time.time()

                # debug output
                sizeInMb = __stat_scan_size / 1024 / 1024
                throughPut = sizeInMb / deltaTime
                # reset byte counter
                __stat_scan_size = 0
                relname = os.path.relpath(dirName, rootDir)
                debug = "[files: {f:5d},  size: {s:8.2f}MB {t:8.2f}MB/s] [{x:60}]".format(f=len(__total_files_list),
                                                                                          s=__total_scan_size / 1024 / 1024,
                                                                                          t=throughPut, x=relname)
                print("\r" + debug, end="\r")

        if (dirName == rootDir):
            print("\r\n")

        return

