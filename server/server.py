import uuid
import hashlib


class GplusItem:

    name = ""
    uuid = None
    parent = None
    remote_sync = None
    checksum = None

    def __init__(self, parent, name):
        self.set_parent(parent)
        self.set_name(name)
        #
        self.uuid = self.create_uuid()
        self.remote_sync = dict()
        self.checksum = self.create_checksum()

    def set_name(self, name):
        self.name = name.replace('/', '')

    def set_parent(self, parent):
        self.parent = parent

    def create_uuid(self):
        return uuid.uuid1()

    def create_checksum(self):
        checksum = hashlib.sha256(self.name.encode('utf-8'))
        return checksum

    def get_full(self):
        if self.parent == None:
            return self.name
        else:
            return self.parent.get_full() + '/' + self.name

    def disp(self):
        print(self.uuid.hex + "\t\t\t" + type(self).__name__ + "\t\t\t" + self.get_full())


class GplusFolder(GplusItem):

    sub_items = list()

    def __init__(self, parent, name):
        super(GplusFolder, self).__init__(parent, name)
        self.sub_items = list()

    def add(self, sub_item):
        self.sub_items.append(sub_item)


class GplusFile(GplusItem):

    file_size = 0
    content = None

    def __init__(self, parent, name):
        super(GplusFile, self).__init__(parent, name)
        self.content = None


class GplusTree:

    root = None

    # g+:/testx/
    def __init__(self, root_str, tree_name):
        self.root = GplusFolder(None, root_str)

    def add_folder(self, parent, folder_name):
        if parent == None:
            parent = self.root

        f = GplusFolder(parent, folder_name)
        parent.add(f)
        return f

    def add_file(self, parent, file_name):
        if parent == None:
            parent = self.root

        if type(parent).__name__ == 'GplusFolder':
            f = GplusFile(parent, file_name)
            parent.add(f)
        else:
            raise Exception('GplusTree.add_file() - parent is not GplusFolder')
            f = None
        return f

    def ls(self, parent=None, ret_list=list(), output=1):
        if parent == None:
            parent = self.root

        ret_list.append(parent)
        if output == 1:
            parent.disp()

        if type(parent).__name__ == 'GplusFolder':
            for s in parent.sub_items:
                self.ls(s, ret_list)

        return ret_list

    def find(self, search_str, parent=None):

        if parent == None:
            parent = self.root

        ret_list = self.__find_recursive(search_str, parent)
        return ret_list

    def __find_recursive(self, search_str, parent=None, ret_list=list(), output=1):

        if parent.name == search_str:
            ret_list.append(parent)
            if output == 1:
                parent.disp()

        if type(parent).__name__ == 'GplusFolder':
            for s in parent.sub_items:
                self.__find_recursive(search_str, s, ret_list)

        return ret_list


# main
g = GplusTree("g+:/testx/", "master")

f1 = g.add_folder(None, "hokus")

f2 = g.add_folder(f1, "pokus")

f3 = g.add_folder(f1, "ixus")

f4 = g.add_file(f3, "testfile.zip")

f5 = g.add_file(f3, "anotherfile.txt")


r = g.ls()

x = g.find('anotherfile.txt')

print(x)

