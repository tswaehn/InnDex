
import os


def run(innDex, res):

    lx = innDex['data']
    for hashKey in lx:
        item = lx[hashKey]

        fname = item['fname']
        ext = os.path.splitext(fname)[1].upper()
        print('found {s}'.format(s=ext))

        if ext not in res:
            res[ext] = list()

        res[ext].append(hashKey)
    return res
