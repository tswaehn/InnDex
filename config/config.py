from tools import my_json


class Config:

    # const
    __CONFIG = "innDex.conf.JSON"
    __CONFIG_VER = "1.0"
    conf = dict()

    def __init__(self, config_filename):
        self.__CONFIG = config_filename
        self.load()
        return

    def load(self):
        print("loading config: {s}".format(s=self.__CONFIG))
        try:
            self.conf = my_json.read(self.__CONFIG)
        except FileNotFoundError:
            print("config not found")
            self.__createNewConfig()

        return 1

    def get(self,  key):

        if key in self.conf:
            return self.conf[key]
        else:
            self.set(key,  None)
            return self.conf[key]

    def set(self,  key,  value):
        self.conf[key] = value
        my_json.write(self.__CONFIG, self.conf)
        return 1

    def __createNewConfig(self):
        print("creating default config")
        self.conf = dict()

        self.set('version', self.__CONFIG_VER)
        self.set('update_index', list({"folder1",  "folder2"}))
        self.set('proc_compare', list({"folder1",  "folder2"}))

        # write
        my_json.write(self.__CONFIG, self.conf)
        # load
        self.conf = my_json.read(self.__CONFIG)

        return 1

