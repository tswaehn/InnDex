from processors import proc_extension, proc_filename
from tools import my_json


def hello():
    print("hello reader")


def exec_all(innDex):

    ix = dict()
    ix = proc_extension.run(innDex, ix)

    ix = proc_filename.run(innDex, ix)

    my_json.write('test.json', ix)
    print(ix)
    return
