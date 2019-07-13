
from readers import proc_extension
from readers import proc_filename
import indexReadWrite


def hello():
    print("hello reader")


def exec_all(innDex):

    ix = dict()
    ix = proc_extension.run(innDex, ix)

    ix = proc_filename.run(innDex, ix)

    indexReadWrite.write('test.json', ix)
    print(ix)
    return
