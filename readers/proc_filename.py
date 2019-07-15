import os
import re

def run(innDex, res):

    lx = innDex['data']
    for hashKey in lx:
        item = lx[hashKey]

        # use relative path / uppercase / no file extension
        rname = item['rname']
        rname = rname.upper()
        rname = os.path.splitext(rname)[0]

        tokens = re.split('[\\ |\\\\|\\.|\\-|_|\\(|\\)|\\[|\\]|\\/]', rname)

        for token in tokens:
            if len(token) == 0:
                continue

            # add token to result list
            __add(res, token, hashKey)

    return res


def __add(res, token, hashKey):

    if token not in res:
        res[token] = list()

    res[token].append(hashKey)

    return res
