
from readers import proc_extension
import indexReadWrite


def hello():
    print("hello reader")


def process_list(innDex):

    ix = dict()
    proc_extension.run(innDex, ix)

    indexReadWrite.write('test.json', ix)
    print(ix)
    return
